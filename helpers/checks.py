from functools import wraps
from flask import current_app, request, Response, abort
import os

#VARIABLES
X_BROKER_API_MAJOR_VERSION = 2
X_BROKER_API_MINOR_VERSION = 15
X_BROKER_API_VERSION_NAME = 'X-Broker-Api-Version'



#API VERSION CHECKING
def api_version_is_valid(api_version):
    version_data = api_version.split('.')
    result = True
    if (float(version_data[0]) < X_BROKER_API_MAJOR_VERSION or
    (float(version_data[0]) == X_BROKER_API_MAJOR_VERSION and
    float(version_data[1]) < X_BROKER_API_MINOR_VERSION)):
                result = False
    return result

def requires_api_version(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_version = request.headers.get('X-Broker-Api-Version')
        if (not api_version or not (api_version_is_valid(api_version))):
            abort(412)
        return f(*args, **kwargs)
    return decorated


#AUTH CHECKS
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    expected_username = os.environ.get('BROKER_USERNAME','admin')
    expected_password = os.environ.get('BROKER_PASSWORD','admin')
    if not (username == expected_username and password == expected_password):
        current_app.logger.warning('Authentication failed')
    return username == expected_username and password == expected_password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
