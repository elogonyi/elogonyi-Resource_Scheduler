import unittest
from app.scheduler import ResourceScheduler

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = ResourceScheduler()

    def test_add_customer(self):
        self.scheduler.add_customer(1, 5, "VIP")
        self.assertEqual(len(self.scheduler.queue), 1)

    def test_assign_tasks(self):
        self.scheduler.add_customer(2, 3, "Normal")
        self.scheduler.assign_tasks()
        agent_tasks = sum([len(agent.tasks) for agent in self.scheduler.agents])
        self.assertGreater(agent_tasks, 0)

if __name__ == '__main__':
    unittest.main()
