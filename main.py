from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from google.cloud import firestore
from api import spin, cashout, initialize_user

# Initialize Firestore DB
db = firestore.Client()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

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
        # Return 204 No Content for preflight requests
        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    try:
        # Get the path of the request
        path = request.path
        # Parse the JSON request body
        request_json = request.get_json()

        print("New entry")
        print(f"Request path: {path}")
        print(f"Request JSON: {request_json}")

        # Route the request to the appropriate function based on the path
        if path == "/spin":
            return_code, ret = spin(request_json, db)
        elif path == "/cashout":
            return_code, ret = cashout(request_json, db)
        elif path == "/initialize":
            return_code, ret = initialize_user(request_json, db)
        else:
            # If the path is not recognized, return a 400 error
            return_code = 400
            ret = {"error": "Invalid endpoint"}

        print(f"Response: {ret}")
        print(f"Return code: {return_code}")

        # Create the response object
        response = make_response(jsonify(ret), return_code)
        response.headers.update(headers)

        return response
    except Exception as e:
        # Log any errors and return a 500 Internal Server Error response
        print(f"Error: {str(e)}")
        response = make_response(jsonify({"error": "Internal Server Error"}), 500)
        response.headers.update(headers)
        return response

# Define the route handlers that call the entry function
@app.route('/spin', methods=['POST', 'OPTIONS'])
@app.route('/cashout', methods=['POST', 'OPTIONS'])
@app.route('/initialize', methods=['POST', 'OPTIONS'])
def route_handler():
    return entry(request)

# Run the application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
