import random
from google.cloud import firestore

# Define the possible symbols and their corresponding rewards
symbols = ['C', 'L', 'O', 'W']
rewards = {'C': 10, 'L': 20, 'O': 30, 'W': 40}

# In-memory store for user credits
user_credits = {}

def get_credits(session_id, db):
    # Retrieve the credits for a session, initializing to 10 if not found
    if session_id not in user_credits:
        doc_ref = db.collection('users').document(session_id)
        doc = doc_ref.get()
        if doc.exists:
            user_credits[session_id] = doc.to_dict().get('credits', 10)
        else:
            user_credits[session_id] = 10  # Initialize with 10 credits
    return user_credits[session_id]

def set_credits(session_id, credits, db):
    # Set the credits for a session and update Firestore
    user_credits[session_id] = credits
    db.collection('users').document(session_id).set({'credits': credits})

def initialize_user(request_json, db):
    try:
        session_id = request_json.get("session_id")
        if not session_id:
            return 400, {"error": "Session ID is required"}

        credits = get_credits(session_id, db)

        response = {
            "credits": credits
        }

        print(f"Initialize response: {response}")

        return 200, response
    except Exception as e:
        print(f"Error in initialize_user function: {str(e)}")
        return 500, {"error": "Internal Server Error"}

def spin(request_json, db):
    try:
        session_id = request_json.get("session_id")
        if not session_id:
            return 400, {"error": "Session ID is required"}

        credits = get_credits(session_id, db)
        if credits <= 0:
            return 400, {"error": "Not enough credits"}

        credits -= 1

        result = [random.choice(symbols) for _ in range(3)]

        if result[0] == result[1] == result[2]:
            reward = rewards[result[0]]
            if credits >= 40 and credits < 60:
                if random.random() < 0.3:
                    result = [random.choice(symbols) for _ in range(3)]
                    reward = rewards[result[0]] if result[0] == result[1] == result[2] else 0
            elif credits >= 60:
                if random.random() < 0.6:
                    result = [random.choice(symbols) for _ in range(3)]
                    reward = rewards[result[0]] if result[0] == result[1] == result[2] else 0
            credits += reward
        else:
            reward = 0

        set_credits(session_id, credits, db)

        response = {
            "slots": result,
            "credits": credits
        }

        print(f"Spin response: {response}")

        return 200, response
    except Exception as e:
        print(f"Error in spin function: {str(e)}")
        return 500, {"error": "Internal Server Error"}

def cashout(request_json, db):
    try:
        session_id = request_json.get("session_id")
        if not session_id:
            return 400, {"error": "Session ID is required"}

        credits = get_credits(session_id, db)
        user_credits[session_id] = 0  # Reset credits
        db.collection('users').document(session_id).set({'credits': 0})

        response = {
            "credits": credits
        }

        print(f"Cashout response: {response}")

        return 200, response
    except Exception as e:
        print(f"Error in cashout function: {str(e)}")
        return 500, {"error": "Internal Server Error"}
