import dash
import dash_html_components as html

import test_runner_components
from sqlalchemy import *
from sqlalchemy.engine import create_engine
# from sqlalchemy.schema import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_bigquery import ARRAY, DATE, RECORD, STRING

# engine = create_engine('bigquery://terra-kernel-k8s',
# credentials_path='/Users/ichang/Downloads/terra-kernel-k8s-bd7b02311de9.json') streamtable = Table(
# 'stream_dataset.streamtable', MetaData(bind=engine), autoload=True) print(streamtable) print(select([func.count(
# '*')], from_obj=streamtable).scalar())
from app import app
from app.bigquery.models.User import User

# app = dash.Dash(__name__)
# app.server.config[
#    'SQLALCHEMY_DATABASE_URI'] = 'bigquery://terra-kernel-k8s/stream_dataset?credentials_path=/Users/ichang/Downloads/terra-kernel-k8s-bd7b02311de9.json'
# db = SQLAlchemy(app.server)


# u1 = User(id='2', first_name='J.', last_name='Thomas', addresses=[{'status': 'active', 'address': '105 Broadway',
#                                                                   'city': 'Cambridge', 'state': 'MA', 'zip': '02142',
#                                                                   'numberOfYears': '3'},
#                                                                  {'status': 'inactive', 'address': '40 Winter St',
#                                                                   'city': 'Cambridge', 'state': 'MA', 'zip': '02141',
#                                                                   'numberOfYears': '1'}
#                                                                  ]
#)
#db.session.add(u1)
#db.session.commit()

user = User.query.filter_by(last_name='Thomas').first()
print(user.id)

app.layout = html.Div([
    html.Div([html.Div("Test tooltip")],
             **{'data-for': 'element-id1', 'data-tip': 'true'}),
    test_runner_components.TooltipsTheme1(
        id='input',
        label='my-label'
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=443, debug=True, ssl_context='adhoc')
