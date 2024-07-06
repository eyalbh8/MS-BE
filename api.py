import random

# Define the possible symbols and their corresponding rewards
symbols = ['C', 'L', 'O', 'W']
rewards = {'C': 10, 'L': 20, 'O': 30, 'W': 40}

# In-memory store for user credits
user_credits = {}

def get_credits(session_id, db):
    """
    Retrieve the credits for a session. If the session does not exist in memory,
    check the Firestore database and initialize to 10 credits if not found.
    """
    if session_id not in user_credits:
        doc_ref = db.collection('users').document(session_id)
        doc = doc_ref.get()
        if doc.exists:
            user_credits[session_id] = doc.to_dict().get('credits', 10)
        else:
            user_credits[session_id] = 10  # Initialize with 10 credits
    return user_credits[session_id]

def set_credits(session_id, credits, db):
    """
    Set the credits for a session in memory and update the Firestore database.
    """
    user_credits[session_id] = credits
    db.collection('users').document(session_id).set({'credits': credits})

def initialize_user(request_json, db):
    """
    Initialize a user by checking if they exist in the Firestore database and
    retrieving their credits. If they do not exist, create a new user document
    with 10 credits.
    """
    try:
        session_id = request_json.get("session_id")
        if not session_id:
            return 400, {"error": "Session ID is required"}

        doc_ref = db.collection('users').document(session_id)
        doc = doc_ref.get()
        if doc.exists:
            credits = doc.to_dict().get('credits', 10)
        else:
            # Create a new user document with 10 credits if it does not exist
            credits = 10
            doc_ref.set({'credits': credits})
            user_credits[session_id] = credits

        response = {
            "credits": credits
        }

        print(f"Initialize response: {response}")

        return 200, response
    except Exception as e:
        print(f"Error in initialize_user function: {str(e)}")
        return 500, {"error": "Internal Server Error"}

def spin(request_json, db):
    """
    Handle the spinning of the slot machine. Deduct 1 credit, randomly generate
    the slot results, apply cheating logic based on the user's credits, and
    update the user's credits accordingly.
    """
    try:
        session_id = request_json.get("session_id")
        if not session_id:
            return 400, {"error": "Session ID is required"}

        credits = get_credits(session_id, db)
        if credits <= 0:
            return 400, {"error": "Not enough credits"}

        # Deduct 1 credit for the spin
        credits -= 1

        # Simulate spinning the slots by randomly selecting symbols
        result = [random.choice(symbols) for _ in range(3)]

        # Calculate the reward based on the spin result
        if result[0] == result[1] == result[2]:
            reward = rewards[result[0]]
            # Implement cheating logic based on the number of credits
            if credits >= 40 and credits < 60:
                if random.random() < 0.3:
                    # Re-roll with a 30% chance if credits are between 40 and 60
                    result = [random.choice(symbols) for _ in range(3)]
                    reward = rewards[result[0]] if result[0] == result[1] == result[2] else 0
            elif credits >= 60:
                if random.random() < 0.6:
                    # Re-roll with a 60% chance if credits are above 60
                    result = [random.choice(symbols) for _ in range(3)]
                    reward = rewards[result[0]] if result[0] == result[1] == result[2] else 0
            credits += reward  # Add the reward to the credits
        else:
            reward = 0

        # Update the credits for the session
        set_credits(session_id, credits, db)

        # Prepare the response
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
    """
    Handle the cashout process by resetting the user's credits to 0 and updating
    the Firestore database.
    """
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
