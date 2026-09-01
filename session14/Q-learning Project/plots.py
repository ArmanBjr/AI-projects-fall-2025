import numpy as np
import matplotlib.pyplot as plt


class Visualization:
    def __init__(self, total_reward, success_rate):
        self.total_reward = total_reward
        self.success_rate = success_rate


    def plot_results(self):
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        
        # Plot 1: Episode rewards
        axes[0, 0].plot(self.total_reward, alpha=0.6, linewidth=0.5)
        axes[0, 0].set_xlabel('Episode')
        axes[0, 0].set_ylabel('Total Reward')
        axes[0, 0].set_title('Episode Rewards')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Moving average of rewards
        window_size = 100
        if len(self.total_reward) >= window_size:
            moving_avg = np.convolve(self.total_reward, np.ones(window_size)/window_size, mode='valid')
            axes[0, 1].plot(range(window_size-1, len(self.total_reward)), moving_avg, 
                        color='red', linewidth=2)
            axes[0, 1].set_xlabel('Episode')
            axes[0, 1].set_ylabel(f'Avg Reward ({window_size} eps)')
            axes[0, 1].set_title('Moving Average of Rewards')
            axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Success rate
        axes[1, 0].plot(self.success_rate, alpha=0.6, linewidth=0.5)
        axes[1, 0].set_xlabel('Episode')
        axes[1, 0].set_ylabel('Success (1=Yes)')
        axes[1, 0].set_title('Episode Success')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Moving average of success rate
        if len(self.success_rate) >= window_size:
            success_avg = np.convolve(self.success_rate, np.ones(window_size)/window_size, mode='valid')
            axes[1, 1].plot(range(window_size-1, len(self.success_rate)), success_avg * 100, 
                        color='green', linewidth=2)
            axes[1, 1].set_xlabel('Episode')
            axes[1, 1].set_ylabel(f'Success Rate % ({window_size} eps)')
            axes[1, 1].set_title('Moving Average Success Rate')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('training_results.png', dpi=100, bbox_inches='tight')
        plt.show()