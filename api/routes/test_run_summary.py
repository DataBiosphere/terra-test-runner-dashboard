import datetime
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
