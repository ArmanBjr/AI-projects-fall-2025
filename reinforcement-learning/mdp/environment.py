from abc import ABC, abstractmethod
from typing import Tuple, List, Any

class Environment(ABC):
    """
    Abstract base class for reinforcement learning environments.
    """
    
    @abstractmethod
    def reset(self) -> Any:
        """
        Reset the environment to initial state.
        
        Returns:
            Initial state
        """
        pass
    
    @abstractmethod
    def step(self, action: int) -> Tuple[Any, float, bool]:
        """
        Take an action in the environment.
        
        Args:
            action: Action to take
            
        Returns:
            Tuple of (next_state, reward, done)
        """
        pass
    
    @abstractmethod
    def get_state(self) -> Any:
        """
        Get the current state of the environment.
        
        Returns:
            Current state representation
        """
        pass
    
    @abstractmethod
    def get_valid_actions(self) -> List[int]:
        """
        Get list of valid actions from current state.
        
        Returns:
            List of valid action indices
        """
        pass
    
    @abstractmethod
    def get_possible_actions(self) -> List[int]:
        """
        Get all possible actions in the environment (regardless of state).
        
        Returns:
            List of all possible action indices
        """
        pass
    
    @abstractmethod
    def is_terminal(self) -> bool:
        """
        Check if current state is terminal.
        
        Returns:
            True if game is over, False otherwise
        """
        pass
    
    @abstractmethod
    def collect_experience(self, num_episodes: int) -> Tuple[dict, List[float]]:
        """
        Collect experience by running random episodes.
        
        Args:
            num_episodes: Number of episodes to run
            
        Returns:
            Tuple of (transitions dictionary, list of episode rewards)
        """
        pass
