from datetime import date

from sqlalchemy import func, and_, not_

from database.models import SummaryTestRun


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
