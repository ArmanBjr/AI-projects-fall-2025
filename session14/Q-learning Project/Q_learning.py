import gymnasium as gym
import minigrid
import numpy as np
from collections import defaultdict
import pickle
import time

from abc import ABC
from reinforcement_learning import ReinforcementLearning

class QLearning(ReinforcementLearning, ABC):
    def __init__(
        self,
        env,
        action_num,
        episodes=8000,
        gamma=0.99,
        learning_rate=0.2,
        epsilon=1.0,
        epsilon_min=0.01,
        epsilon_decay_rate=0.99,
        default_value=0.0
    ):
        super().__init__(env, action_num)

        self.episodes = episodes
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay_rate = epsilon_decay_rate
        self.default_value = default_value

        self.Q = defaultdict(lambda: np.full(action_num, self.default_value))

        self.total_rewards = []
        self.success_rate = []
        self.steps_per_episode = []
        self.best_avg_reward = -float('inf')
        self.no_improvement = 0

    def preprocess_obs(self, obs):
        image = obs['image'] # Image shape: (7,7,3)
        direction = obs['direction'] # 4 main direction: left, right, up, down
        carrying = 1 if image[3, 3, 0] == 10 else 0 # Is carring key or not
        grid_state = tuple(image[:, :, 0].flatten().astype(int)) # Flatten the image width and height

        state_tuple = (direction, carrying) + grid_state # Whole state representation

        return state_tuple


    def reward_shaping(self, reward):
        shaped_reward = reward
    
        # Small penalty for stepping to avoid random walk
        shaped_reward -= 0.001
        
        return shaped_reward
    
    def save_model(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(dict(self.Q), f)
    
    def load_model(self, filename):
        with open(filename, 'rb') as f:
            loaded_model = pickle.load(f)
            self.Q.update(loaded_model)
            
    def select_action(self, state, epsilon):
        q_value = self.Q[state]
        if np.random.random() < epsilon or np.all(q_value == self.default_value):
                return np.random.randint(0, self.action_num)
        
        max_q = np.max(q_value)
        best_actions = np.where(q_value == max_q)[0]
        return np.random.choice(best_actions)
    
    def update(self, state, action, reward, next_state):
        #Q(s, a) ← Q(s, a) + α [ r + γ maxₐ′ Q(s′, a′) − Q(s, a) ]
        #------------------TODO------------------------
        current_q = self.Q[state][action]
        next_q = current_q + self.learning_rate * (reward + self.gamma * np.max(self.Q[next_state]) - current_q)
        self.Q[state][action] = next_q
        #------------------TODO------------------------

    def train(self):
        for episode in range(self.episodes):
                obs, info = self.env.reset(seed=42)
                state = self.preprocess_obs(obs)
                done = False
                terminated = False
                truncated = False

                episode_reward = 0
                steps = 0

                while not done:
                    steps += 1

                    #------------------TODO------------------------
                    # Select action base on epsilon greedy
                    action = self.select_action(state, self.epsilon)

                    # Take action and move one step ahead in environment
                    next_obs , reward, terminated, truncated, info = self.env.step(action)

                    # Preprocess the next observation to achieve next state
                    next_state = self.preprocess_obs(next_obs)

                    # Improve reward via reward engineering(uncomment the line below)
                    new_reward = self.reward_shaping(reward)

                    # Determine termination or truncated status(uncomment the line below)
                    done = (terminated or truncated)

                    # Q_learning update rule
                    self.update(state, action, new_reward, next_state)

                    # Update current state to the next state
                    state = next_state
                    #------------------TODO------------------------

                    episode_reward += new_reward

                    if steps > 200:
                            truncated = True
                            break
                
                #------------------TODO------------------------
                # Apply decay rate to the epsilon
                self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay_rate)
                #------------------TODO------------------------

                # Evaluate success condition
                success = 0
                if episode_reward > 0.5: success += 1
                else : success = 0
                self.success_rate.append(success)

                # Reward and step 
                self.total_rewards.append(episode_reward)
                self.steps_per_episode.append(steps)

                if(episode + 1) % 100 == 0:
                    avg_reward = np.mean(self.total_rewards[-100:])
                    avg_success = np.mean(self.success_rate[-100:]) * 100
                    avg_steps = np.mean(self.steps_per_episode[-100:])
                    
                    print(f"Episode {episode + 1}, "
                        f"Epsilon: {self.epsilon:.3f}, "
                        f"Avg Reward: {avg_reward:.3f}, "
                        f"Success: {avg_success:.1f}%, "
                        f"Avg Steps: {avg_steps:.1f}, "
                        f"States: {len(self.Q)}")
                    
                    if avg_reward > self.best_avg_reward:
                            self.best_avg_reward = avg_reward
                            self.no_improvement = 0
                            self.save_model("best_q_table.pkl")
                    else:
                            self.no_improvement += 1

                    if self.no_improvement > 50:
                            print(f"Early stopping at episode {episode + 1}")
                            break
        
        self.save_model("final_q_table.pkl")
        self.env.close()

        return self.Q, self.total_rewards, self.success_rate
    
    def test(self, env_id, episodes=5, render=True):
        if render:
            test_env = gym.make(env_id, render_mode='human')
        else:
            test_env = gym.make(env_id)
        
        success_count = 0
        total_steps = []
        
        for episode in range(episodes):
            obs, _ = test_env.reset()
            state = self.preprocess_obs(obs)
            
            terminated = False
            truncated = False
            episode_reward = 0
            steps = 0
            
            print(f"\nTest Episode {episode + 1}")
            
            while not (terminated or truncated) and steps < 100:
                if render: 
                    time.sleep(0.05)
                
                # Greedy action
                action = self.select_action(state, epsilon=0.0)
                
                # Take action
                obs, reward, terminated, truncated, _ = test_env.step(action)
                
                # Update state
                state = self.preprocess_obs(obs)
                steps += 1
                episode_reward += reward
            
            
            success = 1 if terminated and episode_reward > 0 else 0
            success_count += success
            total_steps.append(steps)
            
            print(f"  Steps: {steps}, Reward: {episode_reward:.3f}, "
                f"Success: {'Yes' if success else 'No'}")
            
            if render:
                time.sleep(1)
        
        success_rate = (success_count / episodes) * 100
        avg_steps = np.mean(total_steps)
        
        print(f"\nTest Summary: {success_count}/{episodes} successful "
            f"({success_rate:.1f}%), Average Steps: {avg_steps:.1f}")
        
        test_env.close()

