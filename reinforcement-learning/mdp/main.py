import numpy as np
from mdp import MDP
from tetris import MiniTetris
from visualize import AgentVisualizer

def main():
    print("STEP 1: TRAINING VALUE ITERATION AGENT")
    print("="*70)
    
    env = MiniTetris()
    agent = MDP(env, gamma=0.9, theta=1e-6)
    agent.collect_experience(num_episodes=5000)
    
    agent.value_iteration(max_iterations=100_00)    
    
    # agent.value_iteration(max_iterations=2000)
    # agent.extract_policy()
    
    input("\nPress Enter to watch the agent play (3 games)...")
    
    visualizer = AgentVisualizer(agent, delay=0.8)
    
    scores = []
    for game_num in range(3):
        print(f"\n{'='*70}")
        print(f"GAME {game_num + 1}/3")
        print(f"{'='*70}")
        score = visualizer.play_episode(max_steps=500)
        scores.append(score)
        print(f"\n★ Game {game_num + 1} Final Score: {score:.0f}")
        
        if game_num < 2:
            input("\nPress Enter for next game...")
    
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    print(f"\nGame Scores: {[int(s) for s in scores]}")
    print(f"Average Score: {np.mean(scores):.1f}")
    print(f"Best Score: {np.max(scores):.0f}")
    
if __name__ == "__main__":
    main()
