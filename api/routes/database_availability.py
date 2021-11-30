from database.models import SummaryTestRun, db


async def is_available():
    count = SummaryTestRun.query.count()
    return f"SQLALCHEMY_DATABASE_URI={db.get_app().config.get('SQLALCHEMY_DATABASE_URI')};count={count}"
