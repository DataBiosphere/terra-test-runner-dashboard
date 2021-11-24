from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_bigquery import ARRAY, RECORD, STRING, TIMESTAMP, INTEGER, BOOLEAN, FLOAT

db = SQLAlchemy()


# ORM mapping for SUMMARY_testRun table.
class SummaryTestRun(db.Model):
    __tablename__ = "SUMMARY_testRun"
    id = db.Column(STRING, primary_key=True, nullable=False)
    startTimestamp = db.Column(TIMESTAMP, nullable=False)
    endTimestamp = db.Column(TIMESTAMP, nullable=False)
    startUserJourneyTimestamp = db.Column(TIMESTAMP, nullable=False)
    endUserJourneyTimestamp = db.Column(TIMESTAMP, nullable=False)
    testSuiteName = db.Column(STRING, nullable=True)
    testConfiguration = db.Column(RECORD(
        serverSpecificationFile=STRING
    ), nullable=True)
    testScriptResultSummaries = db.Column(ARRAY(
        RECORD(
            testScriptName=STRING,
            totalRun=INTEGER,
            numCompleted=INTEGER,
            numExceptionsThrown=INTEGER,
            isfailure=BOOLEAN,
            numberOfYears=STRING,
            elapsedTimeStatistics=RECORD(
                percentile95=FLOAT
            )
        )
    ), nullable=True)

    def __repr__(self):
        return '<SummaryTestRun %r>' % self.testSuiteName