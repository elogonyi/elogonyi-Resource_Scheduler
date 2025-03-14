from flask import Flask, request, jsonify
from scheduler import ResourceScheduler
import threading
import time

app = Flask(__name__)
scheduler = ResourceScheduler()

# Simulate real-time updates every 5 seconds
def update_status():
    while True:
        scheduler.update_agent_status()
        time.sleep(5)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.json
    customer_id = data['id']
    service_time = data['service_time']
    priority = data['priority']
    scheduler.add_customer(customer_id, service_time, priority)
    return jsonify({"message": "Customer added", "customer": data}), 201

@app.route('/assign_tasks', methods=['GET'])
def assign_tasks():
    scheduler.assign_tasks()
    return jsonify({"message": "Tasks assigned", "agents": scheduler.get_agents_status()}), 200

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"agents": scheduler.get_agents_status()}), 200

if __name__ == '__main__':
    threading.Thread(target=update_status, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)

