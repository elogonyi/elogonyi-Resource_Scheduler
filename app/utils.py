import random

def generate_random_customer():
    return {
        "id": random.randint(1000, 9999),
        "service_time": random.randint(2, 10),
        "priority": random.choice(["VIP", "Corporate", "Normal"])
    }
