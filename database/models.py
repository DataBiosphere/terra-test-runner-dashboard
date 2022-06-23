from datetime import datetime
import pytz, re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
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
        serverSpecificationFile=STRING,
        server=RECORD(
            catalogUri=STRING,
            externalCredentialsManagerUri=STRING,
            workspaceManagerUri=STRING
        )
    ), nullable=True)
    testScriptResultSummaries = db.Column(ARRAY(
        RECORD(
            testScriptName=STRING,
            testScriptDescription=STRING,
            totalRun=INTEGER,
            numCompleted=INTEGER,
            numExceptionsThrown=INTEGER,
            isfailure=BOOLEAN,
            elapsedTimeStatistics=RECORD(
                min=FLOAT,
                max=FLOAT,
                mean=FLOAT,
                standardDeviation=FLOAT,
                median=FLOAT,
                percentile95=FLOAT
            )
        )
    ), nullable=True)
    versionScriptResults = db.Column(ARRAY(
        RECORD(
            gitVersions=ARRAY(
                RECORD(
                    remoteOriginUrl=STRING,
                    branch=STRING,
                    refHeadCommit=STRING,
                    shortRefHeadCommit=STRING
                )
            )
        ),
        RECORD(
            helmVersions=ARRAY(
                RECORD(
                    appName=STRING,
                    helmAppVersion=STRING,
                    helmChartVersion=STRING
                )
            )
        )
    ))

    @hybrid_property
    def serverSpecificationFile(self) -> str:
        return self.testConfiguration['serverSpecificationFile']

    @hybrid_property
    def git_version(self):
        for version in self.versionScriptResults:
            if 'gitVersions' in version:
                if len(version['gitVersions']) > 0:
                    for git in version['gitVersions']:
                        return {
                            'remoteOriginUrl': git['remoteOriginUrl'],
                            'shortRefHeadCommit': git['shortRefHeadCommit']
                        }
        return {}

    @hybrid_property
    def helm_version(self):
        for version in self.versionScriptResults:
            if 'helmVersions' in version:
                if len(version['helmVersions']) > 0:
                    for helm in version['helmVersions']:
                        return {
                            'appName': helm['appName'],
                            'helmAppVersion': helm['helmAppVersion'],
                            'helmChartVersion': helm['helmChartVersion']
                        }
        return {}

    @hybrid_property
    def service_uri_dict(self):
        return {k: v for k, v in self.testConfiguration['server'].items()
                if re.search(".*Uri$", k) and v is not None}

    @hybrid_method
    def match_server_spec(self, spec) -> bool:
        return self.serverSpecificationFile == spec

    @hybrid_method
    def match_date(self, date) -> bool:
        return func.date(self.startTimestamp) == date

    @hybrid_method
    def match_date_range(self, start_date, end_date) -> bool:
        return and_(func.date(self.startTimestamp) >= start_date, func.date(self.startTimestamp) <= end_date)

    @hybrid_method
    def match_today(self) -> bool:
        return func.date(self.startTimestamp) == datetime.now(pytz.timezone('US/Eastern')).date()

    def __repr__(self):
        return '<SummaryTestRun %r %r %r %r %r>' % (
            self.id, self.startTimestamp, self.testSuiteName, self.testScriptResultSummaries[0]['testScriptName'], self.testScriptResultSummaries)
