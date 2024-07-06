import random

# Constants for the slot machine symbols and rewards
symbols = ['C', 'L', 'O', 'W']
rewards = {'C': 10, 'L': 20, 'O': 30, 'W': 40}

# In-memory store for user credits
user_credits = {}

def get_credits(session_id):
    if session_id not in user_credits:
        user_credits[session_id] = 10  # Initialize with 10 credits
    return user_credits[session_id]

def set_credits(session_id, credits):
    user_credits[session_id] = credits

def spin(request_json):
    session_id = request_json.get("session_id")
    if not session_id:
        return 400, {"error": "Session ID is required"}

    credits = get_credits(session_id)
    if credits <= 0:
        return 400, {"error": "Not enough credits"}

    # Deduct 1 credit for the spin
    credits -= 1

    # Simulate spinning the slots
    result = [random.choice(symbols) for _ in range(3)]

    # Calculate the reward
    if result[0] == result[1] == result[2]:
        reward = rewards[result[0]]
        # Cheating logic
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

    set_credits(session_id, credits)

    response = {
        "slots": result,
        "credits": credits
    }

    return 200, response

def cashout(request_json):
    session_id = request_json.get("session_id")
    if not session_id:
        return 400, {"error": "Session ID is required"}

    credits = get_credits(session_id)
    user_credits[session_id] = 0  # Reset credits

    response = {
        "credits": credits
    }

    return 200, response
