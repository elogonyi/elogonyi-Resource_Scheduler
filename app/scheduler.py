import random

class Agent:
    def __init__(self, id):
        self.id = id
        self.tasks = []
        self.is_busy = False
        self.capacity = 3  # Maximum tasks per agent

    def assign_task(self, task):
        if len(self.tasks) < self.capacity:
            self.tasks.append(task)
            self.is_busy = True
            return True
        return False

    def clear_tasks(self):
        self.tasks = []
        self.is_busy = False

class ResourceScheduler:
    def __init__(self):
        self.agents = [Agent(i) for i in range(3)]  # 3 Agents
        self.queue = []

    def add_customer(self, customer_id, service_time, priority):
        self.queue.append({"id": customer_id, "service_time": service_time, "priority": priority})
        self.queue.sort(key=lambda x: (x['priority'], x['service_time']))  # Priority Scheduling

    def assign_tasks(self):
        for agent in self.agents:
            if not agent.is_busy:
                if self.queue:
                    agent.assign_task(self.queue.pop(0))

    def update_agent_status(self):
        for agent in self.agents:
            if agent.tasks:
                agent.tasks.pop(0)  # Simulate task completion
            if not agent.tasks:
                agent.is_busy = False

    def get_agents_status(self):
        return [{"id": agent.id, "tasks": len(agent.tasks), "is_busy": agent.is_busy} for agent in self.agents]
