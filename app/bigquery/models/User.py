from sqlalchemy_bigquery import ARRAY, DATE, RECORD, STRING

from app import db


# ORM Model
class User(db.Model):
    __tablename__ = "streamtable"
    id = db.Column(STRING, primary_key=True, nullable=True)
    first_name = db.Column(STRING, nullable=True)
    last_name = db.Column(STRING, nullable=True)
    dob = db.Column(DATE, nullable=True)
    addresses = db.Column(ARRAY(
        RECORD(
            status=STRING,
            address=STRING,
            city=STRING,
            state=STRING,
            zip=STRING,
            numberOfYears=STRING
        )
    ), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.first_name
