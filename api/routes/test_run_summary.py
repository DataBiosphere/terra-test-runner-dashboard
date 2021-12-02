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
    print(f"{len(summaries)}");
    return summaries
