import numpy as np
from collections import defaultdict
from environment import Environment

class MDP:
    def __init__(self, env: Environment, gamma=0.9, theta=0.01):
        self.env = env
        self.gamma = gamma
        self.theta = theta
        self.U = defaultdict(float)
        self.transitions = defaultdict(list)
        self.policy = {}
        
    def collect_experience(self, num_episodes=5000):
        """Delegate experience collection to the environment."""
        self.transitions, total_rewards = self.env.collect_experience(num_episodes)
        return self.transitions, total_rewards
        
    def value_iteration(self, max_iterations=10000):
        """
        Run value iteration algorithm matching the image pseudocode.
        """
        print("\nRunning Value Iteration (Synchronous)...")
        
        # 1. Identify all unique states
        states = set()
        for (s, a), trans_list in self.transitions.items():
            states.add(s)
            for s_next, _, _ in trans_list:
                states.add(s_next)
        
        print(f"State space size: {len(states)} states")
        
        # Initialize U (self.U) and U' (U_new)
        # self.U is already initialized in __init__
        
        for iteration in range(max_iterations):
            delta = 0
            
            # Create U' (U_new) as a copy of current U to store updates
            # This ensures we calculate updates based on fixed previous values
            U_new = self.U.copy()
            
            for state in states:
                if state is None:
                    continue
                
                # Retrieve U[s] (old value)
                u_old = self.U[state]
                
                # Calculate max_a Q(s,a)
                q_values = []
                
                possible_actions = self.env.get_possible_actions()
                
                # ---------------- TODO -------------------
                    
                    # توضیح transitions:
                    # self.transitions[(state, action)] = [
                    #     (next_state, reward, done),
                    #     ...
                    # ]
                for action in possible_actions:

                    # Get all observed transitions for this (s, a)
                    if (state, action) not in self.transitions:
                        continue

                    trans_list = self.transitions[(state, action)]

                    trans_list_len = len(trans_list)

                    if trans_list_len == 0:
                        continue
                    
                    prob = 1 / trans_list_len

                    q = 0.0

                    # Calculate Q-value: Σ P(s'|s,a) * [R + γ * U[s']]

                    for next_state, reward, done in trans_list:
                        q += prob * (reward if done else (reward + self.gamma * self.U[next_state]))
                    
                    q_values.append(q)

                # U'[s] <- max_a Q(s,a)
                U_new[state] = (max(q_values) if len(q_values) > 0 else u_old)
                
                    # Update delta comparing U'[s] and U[s]
                delta = max(delta, abs(U_new[state] - u_old))
                # ------------------- TODO -------------------
            
            # Update step: U <- U'
            self.U = U_new
            
            if (iteration + 1) % 50 == 0:
                print(f"  Iteration {iteration+1}, Delta: {delta:.6f}")
            
            if delta < self.theta:
                print(f"\n✓ Converged after {iteration+1} iterations!")
                break
        
        print(f"Final delta: {delta:.6f}")
        
    def extract_policy(self):
        """
        Extract greedy policy from value function.
        
        π(s) = argmax_a Q(s,a) = argmax_a Σ_{s'} P(s'|s,a) [R(s,a,s') + γ U(s')]
        """
        print("\nExtracting policy...")
        
        states = set()
        for (s, a), _ in self.transitions.items():
            states.add(s)
        
        for state in states:
            if state is None:
                continue
            
            best_action = None
            best_q = -float('inf')
            
            for action in self.env.get_possible_actions():
                if (state, action) not in self.transitions:
                    continue

                trans_list = self.transitions[(state, action)]
                n_transitions = len(trans_list)
                
                q = 0
                for next_state, reward, done in trans_list:
                    prob = 1.0 / n_transitions
                    if done:
                        q += prob * reward  # Terminal state
                    else:
                        q += prob * (reward + self.gamma * self.U[next_state])
                
                if q > best_q:
                    best_q = q
                    best_action = action
                
            if best_action is not None:
                self.policy[state] = best_action
        
        print(f"Policy defined for {len(self.policy)} states")
        
    def policy_evaluation(self, policy, states, theta=1e-4):
        while True:
            delta = 0
            for state in states:
                action = policy[state]
                u_old = self.U[state]

                # توضیح transitions:
                #                 self.transitions[(state, action)] = [
                #                     (next_state, reward, done),
                #                     ...
                #                 ]

                trans_list = self.transitions[(state, action)]
                n_transitions = len(trans_list)
                
                if n_transitions == 0:
                    continue
                
                prob = 1.0 / n_transitions
                new_u = 0.0

                # ------------------- TODO ------------------
                for next_state, reward, done in trans_list:
                    new_u += prob * (reward if done else (reward + self.gamma * self.U[next_state]))

                self.U[state] = new_u
                delta = max(delta, abs(u_old - new_u))
            if delta < theta:
                break
            # ----------------------- TODO -------------------
    
    def policy_improvement(self, policy, states):
        is_stable = True
        for state in states:
            action_old = policy[state]
            
            best_action = -1
            best_action_value = -float("inf")
            possible_actions = self.env.get_possible_actions()
            for action in possible_actions:
                
                if (state, action) not in self.transitions:
                    continue
                
                # توضیح transitions:
                # self.transitions[(state, action)] = [
                #     (next_state, reward, done),
                #     ...
                # ]

                trans_list = self.transitions[(state, action)]
                n_transitions = len(trans_list)
                
                if n_transitions == 0:
                    continue
                
            # ------------------- TODO -------------------
                q = 0.0
                prob = 1.0 / n_transitions
                for next_state, reward, done in trans_list:
                    q += prob * (reward if done else (reward + self.gamma * self.U[next_state]))



                if q > best_action_value:
                    best_action_value = q
                    best_action = action



            if best_action != action_old:
                is_stable = False

            if best_action != -1:
                policy[state] = best_action
                
                    
                    
            # ------------------- TODO -------------------
        return is_stable
        
    def policy_iteration(self, max_iterations=10000):
        print("\nRunning Policy Iteration...")
        
        states = set()
        for (s, a), trans_list in self.transitions.items():
            states.add(s)
        
        print(f"State space size: {len(states)} states")
        
        policy = {}
        for state in states:
            valid_actions = [
                a for a in self.env.get_possible_actions()
                if (state, a) in self.transitions and len(self.transitions[(state, a)]) > 0
            ]
            if valid_actions:
                policy[state] = np.random.choice(valid_actions)
        
        print(f"Policy initialized for {len(policy)} states")

        for iteration in range(max_iterations):
            states = list(policy.keys())
            
            self.policy_evaluation(policy, states)  
            is_stable = self.policy_improvement(policy, states)
            
            print(f"  Iteration {iteration+1}, Policy stable: {is_stable}")
            
            if is_stable:
                print(f"\n✓ Policy converged after {iteration+1} iterations!")
                break
    
        self.policy = policy
        print(f"Final policy defined for {len(self.policy)} states")