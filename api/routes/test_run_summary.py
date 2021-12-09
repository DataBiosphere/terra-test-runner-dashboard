from datetime import date

from sqlalchemy import func, and_

from database.models import SummaryTestRun


async def test_run_summary(uuid):
    summary = SummaryTestRun.query.filter_by(id=uuid).first()
    return summary


async def test_run_summaries_today():
    summaries = SummaryTestRun.query.filter(
        and_(func.date(SummaryTestRun.startTimestamp) == date.today(),
             SummaryTestRun.testConfiguration['serverSpecificationFile'] == 'workspace-alpha.json')
    ).order_by(SummaryTestRun.startTimestamp.desc()).all()
    return summaries


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
        print(f"{d}")
        return d
    return d
