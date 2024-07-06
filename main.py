from flask import make_response, jsonify
from api import spin, cashout

def entry(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*',
        "Content-Type": "application/json"
    }

    path = request.path
    request_json = request.get_json()

    print("New entry")
    print(request_json)

    if path == "/spin":
        return_code, ret = spin(request_json)

    elif path == "/cashout":
        return_code, ret = cashout(request_json)

    else:
        return_code = 400
        ret = {"error": "Invalid endpoint"}

    print(ret)
    print(return_code)

    response = make_response(jsonify(ret), return_code)
    response.headers = headers

    return response
