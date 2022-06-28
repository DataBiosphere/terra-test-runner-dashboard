import datetime
import re
from datetime import date

import numpy as np
from sqlalchemy import func, and_, not_
from database.models import SummaryTestRun
import pandas as pd

async def test_run_summary(uuid):
    summary = SummaryTestRun.query.filter_by(id=uuid).first()
    return summary


async def test_run_summaries_today():
    return await test_run_summaries(date.today().isoformat(), 'workspace-alpha.json')


async def test_run_summaries(date_val, env_type, testsuite=None):
    if date_val is not None and env_type is not None:
        if testsuite is None:
            summaries = SummaryTestRun.query.filter(
                and_(func.date(SummaryTestRun.startTimestamp) == date.fromisoformat(date_val),
                     SummaryTestRun.testConfiguration['serverSpecificationFile'] == env_type)
            ).order_by(SummaryTestRun.startTimestamp.desc()).all()
        else:
            summaries = SummaryTestRun.query.filter(
                and_(func.date(SummaryTestRun.startTimestamp) == date.fromisoformat(date_val),
                     SummaryTestRun.testConfiguration['serverSpecificationFile'] == env_type,
                     SummaryTestRun.testSuiteName == testsuite)
            ).order_by(SummaryTestRun.startTimestamp.desc()).all()
        return summaries
    return []


async def distinct_testsuite(date_val, env_type):
    if date_val is not None and env_type is not None:
        testsuite = SummaryTestRun.query.filter(
            and_(func.date(SummaryTestRun.startTimestamp) == date.fromisoformat(date_val),
                 SummaryTestRun.testConfiguration['serverSpecificationFile'] == env_type)
        ).order_by(SummaryTestRun.testSuiteName) \
            .with_entities(SummaryTestRun.testSuiteName).distinct().all()
        return [ts for ts, in testsuite]
    return []


async def distinct_test_config(date_val):
    if date_val is not None:
        test_config = SummaryTestRun.query.filter(
            and_(func.date(SummaryTestRun.startTimestamp) == date.fromisoformat(date_val),
                 not_(SummaryTestRun.testConfiguration['serverSpecificationFile'].contains('local')))).order_by(
            SummaryTestRun.testConfiguration['serverSpecificationFile']).with_entities(
            SummaryTestRun.testConfiguration['serverSpecificationFile'],
            func.coalesce(
                SummaryTestRun.testConfiguration['server']['catalogUri'],
                SummaryTestRun.testConfiguration['server']['externalCredentialsManagerUri'],
                SummaryTestRun.testConfiguration['server']['workspaceManagerUri']
            )
        ).distinct().all()
        return test_config
    return []


async def get_server_specs(date_val):
    server_specs = []
    if date_val is not None:
        server_specs = SummaryTestRun.query \
            .with_entities(SummaryTestRun.serverSpecificationFile) \
            .filter(and_(func.date(SummaryTestRun.startTimestamp) == date.fromisoformat(date_val),
                         not_(SummaryTestRun.serverSpecificationFile.contains('local')))) \
            .order_by(SummaryTestRun.serverSpecificationFile).distinct().all()
    return server_specs


async def all_summaries(date_val, env_type):
    d = dict()
    if date_val is not None and env_type is not None:
        summaries = await test_run_summaries(date_val, env_type)
        summaries = sorted(summaries, key=lambda u: u.startTimestamp, reverse=True)
        summaries = sorted(summaries, key=lambda u: u.testSuiteName)
        for s in summaries:
            if s.testSuiteName not in d:
                d[s.testSuiteName] = []
            d[s.testSuiteName].append(s)
        return d
    return d


async def get_test_run_summaries(date_val, server_spec):
    if date_val is None or server_spec is None:
        raise Exception('date_val must be a date string, server_spec cannot be None')

    return SummaryTestRun.query.filter(
        and_(SummaryTestRun.match_date(date_val),
             SummaryTestRun.match_server_spec(server_spec)))\
        .order_by(SummaryTestRun.startTimestamp.desc()).all()


async def all_service_summaries(date_val):
    results = {}
    server_specs = await get_server_specs(date_val)
    for spec in server_specs:
        summaries = await get_test_run_summaries(date_val, spec.serverSpecificationFile)
        results[spec.serverSpecificationFile] = summaries
    return results


async def get_response_time_trends(begin_date, end_date, server_spec):
    data = []
    trends = SummaryTestRun.query \
        .with_entities(
            SummaryTestRun.startUserJourneyTimestamp,
            SummaryTestRun.testScriptResultSummaries
        ) \
        .filter(
            and_(
                SummaryTestRun.match_date_range(begin_date, end_date),
                SummaryTestRun.match_server_spec(server_spec)
            )
        ).order_by(SummaryTestRun.startTimestamp.desc()).all()
    for trend in trends:
        timestamp = trend[0]
        stats = trend[1]
        for stat in stats:
            data.append({
                'timestamp': timestamp,
                'testScriptName': stat['testScriptName'],
                'totalRun': stat['totalRun'],
                'numCompleted': stat['numCompleted'],
                'numExceptionsThrown': stat['numExceptionsThrown'],
                'min': round(stat['elapsedTimeStatistics']['min']),
                'max': round(stat['elapsedTimeStatistics']['max']),
                'mean': round(stat['elapsedTimeStatistics']['mean']),
                'standardDeviation': round(stat['elapsedTimeStatistics']['standardDeviation']),
                'median': round(stat['elapsedTimeStatistics']['median']),
                'percentile95': round(stat['elapsedTimeStatistics']['percentile95']),
            })
    df = pd.DataFrame(data).sort_values('timestamp')
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_convert(tz='US/Eastern')
    df['date'] = [str(ts.month) + '/' + str(ts.day) for ts in df['timestamp']]
    return df


async def get_mc_terra_test_results(begin_date, end_date):
    results = SummaryTestRun.query.filter(SummaryTestRun.match_date_range(begin_date, end_date)) \
        .with_entities(
        SummaryTestRun.versionScriptResults,
        SummaryTestRun.startUserJourneyTimestamp,
        SummaryTestRun.endUserJourneyTimestamp,
        SummaryTestRun.serverSpecificationFile,
        SummaryTestRun.testConfiguration['server'],
        SummaryTestRun.testSuiteName,
        SummaryTestRun.testScriptResultSummaries[0]['testScriptName'],
        SummaryTestRun.testScriptResultSummaries[0]['totalRun'],
        SummaryTestRun.testScriptResultSummaries[0]['numCompleted'],
        SummaryTestRun.testScriptResultSummaries[0]['numExceptionsThrown'],
        SummaryTestRun.testScriptResultSummaries[0]['elapsedTimeStatistics']['min'],
        SummaryTestRun.testScriptResultSummaries[0]['elapsedTimeStatistics']['max'],
        SummaryTestRun.testScriptResultSummaries[0]['elapsedTimeStatistics']['mean'],
        SummaryTestRun.testScriptResultSummaries[0]['elapsedTimeStatistics']['standardDeviation'],
        SummaryTestRun.testScriptResultSummaries[0]['elapsedTimeStatistics']['median'],
        SummaryTestRun.testScriptResultSummaries[0]['elapsedTimeStatistics']['percentile95']) \
        .order_by(
        SummaryTestRun.serverSpecificationFile.asc(),
        SummaryTestRun.testSuiteName.asc(),
        SummaryTestRun.startUserJourneyTimestamp.asc()) \
        .all()
    data = []
    for result in results:
        data.append({
            'spec': result[3],
            'suite': result[5],
            'testScriptName': result[6],
            'totalRun': result[7],
            'numCompleted': result[8],
            'numExceptionsThrown': result[9],
            'min': round(result[10]),
            'max': round(result[11]),
            'mean': round(result[12]),
            'sd': round(result[13]),
            'p50': round(result[14]),
            'p95': round(result[15]),
            'git': git_version(result[0]),
            'helm': helm_version(result[0]),
            'server': service_uri_dict(result[4]),
            'timestamp': result[1]
        })
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_convert(tz='US/Eastern')
    df['date'] = [str(ts.month) + '/' + str(ts.day) for ts in df['timestamp']]

    # Group results for easy parsing using primary and secondary indices
    # e.g.
    # ecm_fullperf = dfg.loc[('workspace-local.json', 'FullIntegration')]
    # print(ecm_fullperf)
    # for script in ecm_fullperf.index.values:
    #    print('{}, {}, {}'.format(script, ecm_fullperf.loc[script]['date'], ecm_fullperf.loc[script]['p95']))

    # for ind in l1:
    #    l2 = dfg.loc[ind].index.values
    #    for ts in l2:
    #        res = dfg.loc[ind].loc[ts]
    #        print('{}, {}, {}, {}'.format(ind, res['git'], res['helm'], res['server']))

    dfg = df.groupby(['spec', 'suite', 'testScriptName']) \
        .agg(
        {
            'totalRun': hist,
            'numCompleted': hist,
            'numExceptionsThrown': hist,
            'min': hist,
            'max': hist,
            'mean': hist,
            'sd': hist,
            'p50': hist,
            'p95': hist,
            'git': 'last',
            'helm': 'last',
            'server': 'last',
            'timestamp': hist,
            'date': hist
        })

    l1 = sorted(list(set([(i[0], i[1]) for i in dfg.index.values])))

    return l1, dfg


def hist(s):
    return tuple(s.values)


def git_version(versions) -> dict:
    for version in versions:
        if 'gitVersions' in version:
            if len(version['gitVersions']) > 0:
                for git in version['gitVersions']:
                    return {
                        'remoteOriginUrl': git['remoteOriginUrl'],
                        'branch': git['branch'],
                        'refHeadCommit': git['refHeadCommit'],
                        'shortRefHeadCommit': git['shortRefHeadCommit']
                    }
    return {}


def helm_version(versions) -> dict:
    for version in versions:
        if 'helmVersions' in version:
            if len(version['helmVersions']) > 0:
                for helm in version['helmVersions']:
                    return {
                        'appName': helm['appName'],
                        'helmAppVersion': helm['helmAppVersion'],
                        'helmChartVersion': helm['helmChartVersion']
                    }
    return {}


def service_uri_dict(server):
    return {k: v for k, v in server.items()
            if re.search(".*Uri$", k) and v is not None}