import numpy as np
from typing import Tuple, List
from collections import defaultdict
from environment import Environment

class MiniTetris(Environment):
    """
    Board: 4 wide × 6 tall
    Pieces: I (2 blocks vertical), Z (2 blocks horizontal), H (2 blocks horizontal)
    State: Column heights [h0, h1, h2, h3] where each h in [0, 6]
    
    Board encoding:
    0 = empty
    2 = I-piece block (cyan) - 2 blocks vertical
    3 = Z-piece block (red) - 2 blocks horizontal (Rhode Island Z)
    4 = H-piece block (yellow) - 2 blocks horizontal
    """
    
    def __init__(self, width=4, height=6):
        self.width = width
        self.height = height
        self.reset()
        
    def reset(self):
        """Reset the game to initial state."""
        self.board = np.zeros((self.height, self.width), dtype=int)
        self.current_piece = self._generate_piece()
        self.next_piece = self._generate_piece()
        self.score = 0
        self.game_over = False
        return self.get_state()
    
    def _generate_piece(self):
        """
        Generate a random piece.
        1 = I-piece (2 blocks vertical)
        2 = Z-piece (2 blocks horizontal, Rhode Island Z)
        3 = H-piece (2 blocks horizontal)
        """
        return np.random.choice([1, 2, 3])  # I, Z, H pieces
    
    def get_state(self):
        """
        Get current state as tuple of column heights.
        
        Returns:
            Tuple of (h0, h1, h2, h3, h4, h5, piece_type)
        """
        heights = []
        for col in range(self.width):
            height = 0
            for row in range(self.height):
                if self.board[row, col] > 0: 
                    height = self.height - row
                    break
            heights.append(height)
        
        return tuple(heights + [self.current_piece])
    
    def get_valid_actions(self):
        """Get list of valid column placements for current piece."""
        valid = []
        for col in range(self.width):
            if self._can_place(col):
                valid.append(col)
        return valid
    
    def _can_place(self, col):
        """Check if current piece can be placed in given column."""
        height = self._get_column_height(col)
        
        if self.current_piece == 1:  # I-piece (2 blocks vertical)
            return height + 1 < self.height
        elif self.current_piece == 2:  # Z-piece (diagonal shape: top-left, bottom-right)
            # Z-piece occupies two columns:
            # - Left column (col): top block
            # - Right column (col+1): bottom block
            if col >= self.width - 1:  # Can't place if last column
                return False
            height_left = self._get_column_height(col)
            height_right = self._get_column_height(col + 1)
            # Bottom-right block will be placed on top of right column
            row_bottom = self.height - height_right - 1
            # Top-left block will be one row above bottom-right
            row_top = row_bottom - 1
            # Check if we have space and if left column position is free
            if row_top < 0 or row_bottom < 0:
                return False
            # Check if left column is free at row_top position
            # height_left tells us the first occupied row from bottom
            # row_top is the position from top where we want to place
            # Convert to check: the spot must be above the current column height
            required_left_height = self.height - row_top
            return required_left_height > height_left
        elif self.current_piece == 3:  # H-piece (2 blocks horizontal)
            # H-piece occupies two columns side-by-side
            if col >= self.width - 1:  # Can't place if last column
                return False
            height_left = self._get_column_height(col)
            height_right = self._get_column_height(col + 1)
            # Both blocks are on the same level, need space above the higher column
            max_height = max(height_left, height_right)
            return max_height < self.height
        
        return False
    
    def _get_column_height(self, col):
        """Get the current height of a column."""
        for row in range(self.height):
            if self.board[row, col] > 0:  # Any block type
                return self.height - row
        return 0
    
    def step(self, action):
        """
        Take an action (place piece in column).
        
        Args:
            action: Column index (0 to width-1)
            
        Returns:
            state, reward, done
        """
        if self.game_over:
            return self.get_state(), 0, True
        
        if action not in self.get_valid_actions():
            self.game_over = True
            return self.get_state(), -10, True
        
        # Place the piece
        height = self._get_column_height(action)
        
        if self.current_piece == 1:  # I-piece (2 blocks vertical)
            row1 = self.height - height - 1
            row2 = self.height - height - 2
            if row2 < 0:
                self.game_over = True
                return self.get_state(), -10, True
            
            self.board[row1, action] = 2  # Mark as I-piece
            self.board[row2, action] = 2  # Mark as I-piece
            
        elif self.current_piece == 2:  # Z-piece (diagonal shape)
            if action >= self.width - 1:
                self.game_over = True
                return self.get_state(), -10, True
            
            height_left = self._get_column_height(action)
            height_right = self._get_column_height(action + 1)
            
            # Bottom-right block sits on top of right column
            row_bottom = self.height - height_right - 1
            # Top-left block is one row above bottom-right
            row_top = row_bottom - 1
            
            if row_top < 0 or row_bottom < 0:
                self.game_over = True
                return self.get_state(), -10, True
            
            # Verify that left column is free at row_top position
            required_left_height = self.height - row_top
            if required_left_height <= height_left:
                # Position is already occupied
                self.game_over = True
                return self.get_state(), -10, True
            
            self.board[row_top, action] = 3        # Top-left block
            self.board[row_bottom, action + 1] = 3  # Bottom-right block
            
        elif self.current_piece == 3:  # H-piece (2 blocks horizontal)
            if action >= self.width - 1:
                self.game_over = True
                return self.get_state(), -10, True
            
            height_left = self._get_column_height(action)
            height_right = self._get_column_height(action + 1)
            
            # Both blocks must be placed at the same row (on top of the higher column)
            max_height = max(height_left, height_right)
            row = self.height - max_height - 1
            
            if row < 0:
                self.game_over = True
                return self.get_state(), -10, True
            
            self.board[row, action] = 4       # Left block
            self.board[row, action + 1] = 4   # Right block (same row)
        else:
            self.game_over = True
            return self.get_state(), -10, True
        
        
        
        
        rows_cleared = self._clear_rows()
        
        reward = rows_cleared * 10  
        reward += 1
        
        max_height = max(self._get_column_height(c) for c in range(self.width))
        if max_height >= self.height:
            self.game_over = True
            reward -= 20
        
        self.score += reward
        
        self.current_piece = self.next_piece
        self.next_piece = self._generate_piece()
        
        return self.get_state(), reward, self.game_over
    
    def _clear_rows(self):
        """Clear completed rows and return count."""
        rows_cleared = 0
        row = self.height - 1
        
        while row >= 0:
            if np.all(self.board[row, :] > 0):  # Check any block type
                self.board = np.delete(self.board, row, axis=0)
                self.board = np.vstack([np.zeros((1, self.width), dtype=int), self.board])
                rows_cleared += 1
            else:
                row -= 1
        
        return rows_cleared
    
    def get_possible_actions(self) -> List[int]:
        """
        Get all possible actions in the environment.
        
        Returns:
            List of all possible action indices (columns where pieces can be placed)
        """
        return list(range(self.width))
    
    def is_terminal(self) -> bool:
        """
        Check if current state is terminal.
        
        Returns:
            True if game is over, False otherwise
        """
        return self.game_over
    
    def collect_experience(self, num_episodes: int) -> Tuple[dict, List[float]]:
        """
        Collect experience by running random episodes.
        
        Args:
            num_episodes: Number of episodes to run
            
        Returns:
            Tuple of (transitions dictionary, list of episode rewards)
        """
        print(f"Collecting {num_episodes} episodes of random experience...")
        
        transitions = defaultdict(list)
        total_rewards = []
        
        for episode in range(num_episodes):
            state = self.reset()
            episode_reward = 0
            steps = 0
            
            while not self.game_over and steps < 100:
                valid_actions = self.get_valid_actions()
                
                if not valid_actions:
                    break
                
                action = np.random.choice(valid_actions)
                next_state, reward, done = self.step(action)
                
                transitions[(state, action)].append((next_state, reward, done))
                
                episode_reward += reward
                state = next_state
                steps += 1
            
            total_rewards.append(episode_reward)
            
            if (episode + 1) % 10000 == 0:
                avg_reward = np.mean(total_rewards[-100:])
                print(f"  Episode {episode+1}/{num_episodes}, Avg Reward: {avg_reward:.2f}")
        
        print(f"\nCollected {len(transitions)} unique (state, action) pairs")
        print(f"Average random reward: {np.mean(total_rewards):.2f}")
        
        return transitions, total_rewards
