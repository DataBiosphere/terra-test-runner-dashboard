import asyncio

from flask import request, make_response, Blueprint
from sqlalchemy.exc import DatabaseError

from api.routes.database_availability import is_available
from api.routes.test_run_summary import test_run_summary, test_run_summaries_today

workspacemanager = Blueprint('workspacemanager', __name__)


# This endpoint can be used by a Kubernetes backend config for health check purpose
@workspacemanager.route('/monitor', methods=['GET'])
async def monitor():
    try:
        if request.method == 'GET':
            print(f"{request.method} {request.path}")
            s = await asyncio.wait_for(is_available(), timeout=10)
            response = make_response(s, 200)
            response.headers['Content-Type'] = 'text/html'
            return response
        else:
            raise ValueError(f"{request.method} method not recognized.")
    except asyncio.TimeoutError:
        response = make_response('TimeoutError', 200)
        response.headers['Content-Type'] = 'text/html'
        return response
    except ValueError as e:
        response = make_response(f"ValueError: {str(e)}", 200)
        response.headers['Content-Type'] = 'text/html'
        return response
    except DatabaseError as e:
        response = make_response(f"DatabaseError: {str(e)}", 200)
        response.headers['Content-Type'] = 'text/html'
        return response
    except FileNotFoundError as e:
        response = make_response(f"FileNotFoundError: {str(e)}", 200)
        response.headers['Content-Type'] = 'text/html'
        return response


# endpoint for retrieving test run summary by id
@workspacemanager.route('/summary/<string:uuid>', methods=['GET'])
async def get_test_summary(uuid):
    try:
        if request.method == 'GET':
            u = await asyncio.wait_for(test_run_summary(uuid), timeout=10)
            stats = u.testScriptResultSummaries[0]['elapsedTimeStatistics']
            response = make_response(f"{u.id}, {u.testSuiteName}, \
            {u.testConfiguration['serverSpecificationFile']}, {stats['percentile95']}", 200)
            response.headers['Content-Type'] = 'text/html'
            return response
        else:
            raise ValueError(f"{request.method} method not recognized.")
    except AttributeError as e:
        response = make_response(f"ValueError: {str(e)}", 200)
        response.headers['Content-Type'] = 'text/html'
        return response
    except asyncio.TimeoutError:
        response = make_response('TimeoutError', 200)
        response.headers['Content-Type'] = 'text/html'
        return response
    except ValueError as e:
        response = make_response(f"ValueError: {str(e)}", 200)
        response.headers['Content-Type'] = 'text/html'
        return response


# endpoint for retrieving test run summary by id
@workspacemanager.route('/summaries/today', methods=['GET'])
async def get_test_summaries_today():
    try:
        if request.method == 'GET':
            summaries = await asyncio.wait_for(test_run_summaries_today(), timeout=10)
            s = "".join([f"{u.id}, {u.testSuiteName}, {u.testConfiguration['serverSpecificationFile']}, \
            {u.testScriptResultSummaries[0]['testScriptName']}, {u.testScriptResultSummaries[0]['elapsedTimeStatistics']['percentile95']}"
                         for u in summaries])
            # stats = u.testScriptResultSummaries[0]['elapsedTimeStatistics']
            # response = make_response(f"{u.id}, {u.testSuiteName}, \
            # {u.testConfiguration['serverSpecificationFile']}, {stats['percentile95']}", 200)
            response = make_response(s, 200)
            response.headers['Content-Type'] = 'text/html'
            return response
        else:
            raise ValueError(f"{request.method} method not recognized.")
    except AttributeError as e:
        response = make_response(f"ValueError: {str(e)}", 200)
        response.headers['Content-Type'] = 'text/html'
        return response
    except asyncio.TimeoutError:
        response = make_response('TimeoutError', 200)
        response.headers['Content-Type'] = 'text/html'
        return response
    except ValueError as e:
        response = make_response(f"ValueError: {str(e)}", 200)
        response.headers['Content-Type'] = 'text/html'
        return response
