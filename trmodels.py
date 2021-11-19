from flask_sqlalchemy.model import Model
from sqlalchemy import Column
from sqlalchemy_bigquery import ARRAY, DATE, RECORD, STRING

# ORM Model
class Person(Model):
    __tablename__ = "streamtable"
    id = Column(STRING, nullable=True)
    first_name = Column(STRING, nullable=True)
    last_name = Column(STRING, nullable=True)
    dob = Column(DATE, nullable=True)
    addresses = Column(ARRAY(
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
        return '<Person %r>' % self.first_name
