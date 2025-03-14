from flask import Flask, request, jsonify
from flask_cors import CORS
from scheduler import ResourceScheduler
import threading
import time
import signal
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration
scheduler = ResourceScheduler()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Event for stopping the background thread gracefully
stop_event = threading.Event()

# Periodic update function
def update_status():
    while not stop_event.is_set():
        scheduler.update_agent_status()
        time.sleep(5)

@app.before_first_request
def start_update_thread():
    """Starts background thread when the first request is received."""
    logging.info("Starting background update thread...")
    thread = threading.Thread(target=update_status, daemon=True)
    thread.start()

@app.route('/add_customer', methods=['POST'])
def add_customer():
    """Endpoint to add a customer to the scheduler."""
    data = request.get_json()
    
    if not data or 'id' not in data or 'service_time' not in data or 'priority' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        customer_id = int(data['id'])
        service_time = float(data['service_time'])
        priority = int(data['priority'])
    except ValueError:
        return jsonify({"error": "Invalid data types"}), 400

    scheduler.add_customer(customer_id, service_time, priority)
    logging.info(f"Customer {customer_id} added with priority {priority}.")
    return jsonify({"message": "Customer added", "customer": data}), 201

@app.route('/assign_tasks', methods=['GET'])
def assign_tasks():
    """Assigns tasks to available agents."""
    scheduler.assign_tasks()
    logging.info("Tasks assigned to agents.")
    return jsonify({"message": "Tasks assigned", "agents": scheduler.get_agents_status()}), 200

@app.route('/status', methods=['GET'])
def status():
    """Fetches the status of all agents."""
    return jsonify({"agents": scheduler.get_agents_status()}), 200

def shutdown_server():
    """Handles server shutdown gracefully."""
    logging.info("Shutting down server...")
    stop_event.set()

# Handle SIGINT (Ctrl+C) for a clean exit
signal.signal(signal.SIGINT, lambda sig, frame: shutdown_server())

if __name__ == '__main__':
    logging.info("Starting Flask server on port 5000...")
    app.run(host='0.0.0.0', port=5000)
