import matplotlib.pyplot as plt
import numpy as np
from mdp import MDP
from tetris import MiniTetris

def generate_plots():
    print("Initializing Environment and Agent...")
    env = MiniTetris()
    # Using specific params from your main.py
    agent = MDP(env, gamma=0.9, theta=1e-10)

    # 1. Collect Data (Smaller batch for quick plotting, or load your pickle if you have one)
    print("Collecting experience (10,000 episodes for visualization)...")
    transitions, random_rewards = agent.collect_experience(num_episodes=100000)
    
    # 2. Train (Value Iteration for speed in this demo)
    print("Running Value Iteration...")
    agent.value_iteration(max_iterations=500)
    agent.extract_policy()

    # 3. Play Games with Trained Agent
    print("Playing validation games...")
    trained_scores = []
    for _ in range(100):
        # We simulate play_episode without visualization for speed
        state = env.reset()
        score = 0
        done = False
        steps = 0
        while not done and steps < 200:
            valid_actions = env.get_valid_actions()
            if not valid_actions: break
            
            # Policy Lookup
            if state in agent.policy and agent.policy[state] in valid_actions:
                action = agent.policy[state]
            else:
                action = np.random.choice(valid_actions)
                
            state, reward, done = env.step(action)
            score += reward
            steps += 1
        trained_scores.append(score)

    # --- PLOTTING ---
    plt.figure(figsize=(15, 10))

    # Plot A: Value Function Intuition (Max Height vs Value)
    plt.subplot(2, 2, 1)
    max_heights = []
    values = []
    
    for state, val in agent.U.items():
        # State structure is (h0, h1, h2, h3, piece_type)
        # We slice [:-1] to get just heights
        heights = state[:-1]
        max_h = max(heights)
        max_heights.append(max_h)
        values.append(val)
        
    plt.scatter(max_heights, values, alpha=0.1, c='blue')
    plt.title("Do Taller Boards have Lower Values?")
    plt.xlabel("Max Column Height")
    plt.ylabel("Learned Value (U)")
    plt.grid(True, alpha=0.3)

    # Plot B: Score Distribution
    plt.subplot(2, 2, 2)
    plt.hist(random_rewards, bins=20, alpha=0.5, label='Random Agent', density=True, color='gray')
    plt.hist(trained_scores, bins=20, alpha=0.5, label='Trained Agent', density=True, color='green')
    plt.title("Performance Comparison")
    plt.xlabel("Game Score")
    plt.ylabel("Density")
    plt.legend()

    # Plot C: Value Heatmap by Column Difference (Bumpiness)
    # Checks if the agent prefers "flat" boards
    plt.subplot(2, 2, 3)
    bumpiness = []
    vals_for_bump = []
    for state, val in agent.U.items():
        heights = state[:-1]
        # Calculate sum of absolute differences between adjacent columns
        bump = sum(abs(heights[i] - heights[i+1]) for i in range(len(heights)-1))
        bumpiness.append(bump)
        vals_for_bump.append(val)
        
    plt.scatter(bumpiness, vals_for_bump, alpha=0.1, c='red')
    plt.title("Value vs. Board Bumpiness")
    plt.xlabel("Bumpiness (Sum of adj height diffs)")
    plt.ylabel("Learned Value (U)")
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 4)
    avg_heights = []
    values_for_avg = []
    
    for state, val in agent.U.items():
        # state[:-1] gets the (h0, h1, h2, h3) tuple
        heights = state[:-1]
        avg_h = sum(heights) / len(heights)
        avg_heights.append(avg_h)
        values_for_avg.append(val)
        
    plt.scatter(avg_heights, values_for_avg, alpha=0.1, c='purple')
    plt.title("Value vs. Average Board Height")
    plt.xlabel("Average Column Height")
    plt.ylabel("Learned Value (U)")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
    print("Plots generated.")

if __name__ == "__main__":
    generate_plots()