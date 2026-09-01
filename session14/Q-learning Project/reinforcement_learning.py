from abc import ABC, abstractmethod

class ReinforcementLearning(ABC):
    def __init__(self, env, action_num):
        self.env = env
        self.action_num = action_num

    @abstractmethod
    def select_action(self, state, epsilon):
        pass

    @abstractmethod
    def update(self, state, action, reward, next_state, done):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def test(self, env_id, episodes=5, render=True):
        pass
