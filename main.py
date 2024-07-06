from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from api import spin, cashout

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

@app.route('/spin', methods=['POST', 'OPTIONS'])
@app.route('/cashout', methods=['POST', 'OPTIONS'])
def entry(request):
    """Responds to any HTTP request."""
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    try:
        path = request.path
        request_json = request.get_json()

        print("New entry")
        print(f"Request path: {path}")
        print(f"Request JSON: {request_json}")

        if path == "/spin":
            return_code, ret = spin(request_json)
        elif path == "/cashout":
            return_code, ret = cashout(request_json)
        else:
            return_code = 400
            ret = {"error": "Invalid endpoint"}

        print(f"Response: {ret}")
        print(f"Return code: {return_code}")

        response = make_response(jsonify(ret), return_code)
        response.headers.update(headers)

        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        response = make_response(jsonify({"error": "Internal Server Error"}), 500)
        response.headers.update(headers)
        return response

if __name__ == '__main__':
    app.run(debug=True)
