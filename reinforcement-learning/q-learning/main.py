import gymnasium as gym
import minigrid
from Q_learning import QLearning
from plots import Visualization

def main():
    # Environment Setup
    env_id = 'MiniGrid-DoorKey-6x6-v0'
    env = gym.make(env_id)

    action_num = env.action_space.n
    print(f"Action Space: {action_num}")

    agent = QLearning(env, action_num=action_num)
    
    # Train the Agent
    print("Start Training.....")
    Q_table, total_reward, success_rate = agent.train()

    # Plot the training result
    v = Visualization(total_reward=total_reward, success_rate=success_rate)
    v.plot_results()

    # Load and test the policy
    agent.load_model("best_q_table.pkl") 
    print("Model loaded.....")
    print("Testing learned policy.....")
    agent.test(env_id, episodes=5, render=True)


if __name__ == "__main__":
    main()


