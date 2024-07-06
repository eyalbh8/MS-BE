import random

# Define the possible symbols and their corresponding rewards
symbols = ['C', 'L', 'O', 'W']
rewards = {'C': 10, 'L': 20, 'O': 30, 'W': 40}

# In-memory store for user credits
user_credits = {}

def get_credits(session_id):
    # Retrieve the credits for a session, initializing to 10 if not found
    if session_id not in user_credits:
        user_credits[session_id] = 10  # Initialize with 10 credits
    return user_credits[session_id]

def set_credits(session_id, credits):
    # Set the credits for a session
    user_credits[session_id] = credits

def spin(request_json):
    try:
        # Retrieve the session ID from the request JSON
        session_id = request_json.get("session_id")
        if not session_id:
            # Return 400 error if session ID is not provided
            return 400, {"error": "Session ID is required"}

        # Get the current credits for the session
        credits = get_credits(session_id)
        if credits <= 0:
            # Return 400 error if there are not enough credits
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
        set_credits(session_id, credits)

        # Prepare the response
        response = {
            "slots": result,
            "credits": credits
        }

        print(f"Spin response: {response}")

        return 200, response
    except Exception as e:
        # Log any errors and return a 500 Internal Server Error response
        print(f"Error in spin function: {str(e)}")
        return 500, {"error": "Internal Server Error"}

def cashout(request_json):
    try:
        # Retrieve the session ID from the request JSON
        session_id = request_json.get("session_id")
        if not session_id:
            # Return 400 error if session ID is not provided
            return 400, {"error": "Session ID is required"}

        # Get the current credits for the session
        credits = get_credits(session_id)
        # Reset the credits for the session
        user_credits[session_id] = 0

        # Prepare the response
        response = {
            "credits": credits
        }

        print(f"Cashout response: {response}")

        return 200, response
    except Exception as e:
        # Log any errors and return a 500 Internal Server Error response
        print(f"Error in cashout function: {str(e)}")
        return 500, {"error": "Internal Server Error"}
