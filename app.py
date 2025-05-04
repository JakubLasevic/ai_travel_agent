import os
from flask import Flask, render_template, request, jsonify, session
from ai_logic import Chatbot 
from datetime import timedelta
import traceback 

# --- Instantiate Chatbot Globally ---
# This loads the data once when the Flask app starts.
try:
    print("Attempting to initialize Chatbot globally...")
    chatbot = Chatbot() # Instantiates and loads data via __init__
    if chatbot.df.empty:
        print("--- CRITICAL WARNING: Chatbot initialized globally BUT DataFrame is empty. Check CSV paths/content and logs in ai_logic.py. ---")
    else:
         print("--- Chatbot initialized globally with data successfully. ---")
except Exception as e:
    print(f"--- CRITICAL ERROR: Failed to initialize Chatbot globally: {e} ---")
    print(traceback.format_exc())
    chatbot = None


# --- Flask App Setup ---
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'a-very-secret-key-for-dev')
app.permanent_session_lifetime = timedelta(minutes=30)

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# --- Routes ---

@app.route('/')
def index():
    """Renders the main chat page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handles general chat messages using the Chatbot's process_message."""
    # Check if the global chatbot instance failed to initialize
    if chatbot is None:
        print("Error in /chat: Global chatbot instance is None.")
        return jsonify({"error": "Chatbot service is unavailable due to initialization failure."}), 503
    if chatbot.df.empty:
        print("Error in /chat: Global chatbot DataFrame is empty.")
        return jsonify({"error": "Chatbot data is currently unavailable."}), 503

    try:
        user_message = request.json.get('message')
        if not user_message:
             return jsonify({"error": "No message provided."}), 400

        session.permanent = True 

        # Retrieve context from session or initialize if not present
        context = session.get('context', {
            'suitable_for': [], 
            'style': [],
            'intents': [],
            'type': None,
            'budget': None
        })

       
        ai_response_text, locations_list = chatbot.process_message(user_message, context)

        response_data = {
            "response": ai_response_text,
            "locations": locations_list  # List of dicts for buttons
        }

        # Store the potentially updated context back into the session
        session['context'] = context

        return jsonify(response_data)

    except Exception as e:
        print(f"Error in /chat endpoint: {e}\n{traceback.format_exc()}")
        return jsonify({"error": "An internal error occurred during chat processing."}), 500


@app.route('/location_details', methods=['POST'])
def location_details():
    """Handles requests for details about a specific location."""
    # Check if the global chatbot instance failed to initialize or has no data
    if chatbot is None:
        print("Error in /location_details: Global chatbot instance is None.")
        return jsonify({"error": "Chatbot service is unavailable due to initialization failure."}), 503
    if chatbot.df.empty:
        print("Error in /location_details: Global chatbot DataFrame is empty.")
        return jsonify({"error": "Chatbot data is currently unavailable."}), 503

    try:
        data = request.get_json()
        location_name = data.get('location_name')

        if not location_name:
            return jsonify({"error": "Missing 'location_name' in request."}), 400

        print(f"Received request for details: {location_name}")

        # Find location data using the chatbot's method
        location_data = chatbot.get_location_data_by_name(location_name) # Method from ai_logic.py

        if location_data is None:
            print(f"Location not found via get_location_data_by_name: {location_name}")
            # Provide a more specific error message if location not found
            return jsonify({"error": f"Details not found for location '{location_name}'. It might not be in my database."}), 404

        # Get description using the chatbot's method
        description = chatbot.get_description(location_data) # Method from ai_logic.py

        # Get POIs (stored as a list of dicts in the DataFrame row)
        pois = location_data.get('points_of_interest', [])
        # Basic validation that POIs are a list
        if not isinstance(pois, list):
             print(f"Warning: POIs for {location_name} were not a list. Resetting to empty.")
             pois = []

        response_payload = {
            "description": description,
            "points_of_interest": pois
        }
      
        return jsonify(response_payload)

    except Exception as e:
        location_name_for_error = request.json.get('location_name', 'Unknown Location') if request.is_json else 'Unknown Location'
        print(f"Error in /location_details endpoint for {location_name_for_error}: {e}\n{traceback.format_exc()}")
        return jsonify({"error": "An internal server error occurred while fetching location details."}), 500


@app.route('/reset_session', methods=['GET'])
def reset_session():
    """Clears the user's session data."""
    session.clear()
    print("Session cleared.")
    return jsonify({"message": "Session cleared successfully."})



# --- Main execution ---
if __name__ == '__main__':
    # Check if chatbot failed initialization before running
    if chatbot is None:
        print("\n--- APPLICATION FAILED TO START: Chatbot could not be initialized. Check logs above. ---\n")
    elif chatbot.df.empty:
         print("\n--- APPLICATION WARNING: Chatbot initialized but data is empty. App will run but may lack functionality. Check CSV files and paths. ---\n")
    else:
         print("\n--- Chatbot initialized successfully. Starting Flask app... ---\n")

    # Use host='0.0.0.0' to make it accessible on your network
    # Debug=True MUST be False in production
    app.run(debug=True, host='0.0.0.0', port=5001)