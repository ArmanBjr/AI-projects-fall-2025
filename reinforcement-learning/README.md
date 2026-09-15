# Reinforcement Learning

Two agents: one that is handed the model, and one that has to learn without it.

## `mdp/` — Value iteration on mini-Tetris

The transition model is estimated by sampling the environment, then solved exactly.

1. `collect_experience()` plays random episodes to estimate transition probabilities and
   rewards
2. `value_iteration()` sweeps until the value function converges (`theta = 1e-6`,
   `gamma = 0.9`)
3. A greedy policy is extracted and rendered play-by-play

```bash
python main.py
```

Trains, then pauses before visualising three games.

| File | Role |
|------|------|
| `mdp.py` | Value iteration and policy extraction |
| `tetris.py` | `MiniTetris` environment |
| `environment.py` | Environment wrapper |
| `visualize.py` | Play-by-play renderer |
| `analysis.py` | Convergence analysis |
| `demo_states.py` | Inspect values for hand-constructed board states |
| `report.pdf` | Write-up |

## `q-learning/` — Q-learning on MiniGrid DoorKey

Model-free control on `MiniGrid-DoorKey-6x6-v0`, where the agent must pick up a key, unlock
a door and reach the goal.

- Tabular Q-learning: `Q(s,a) ← Q(s,a) + α[r + γ·maxₐ′ Q(s′,a′) − Q(s,a)]`
- ε-greedy exploration with decay, falling back to a random action when a state is unvisited
- State abstraction from the agent's view and facing direction
- Best-performing table checkpointed during training

```bash
pip install -r requirements.txt
python main.py
```

Trains, plots reward and success-rate curves, then reloads the best policy and renders five
test episodes.

| File | Role |
|------|------|
| `Q_learning.py` | Agent — action selection, update rule, save/load |
| `reinforcement_learning.py` | Training loop |
| `plots.py` | Reward and success-rate curves |
| `training_results.png` | Example training run |
| `report.pdf` | Write-up |
| `project-brief-fa.pdf` | Original project brief (Persian) |

> `main.py` loads `best_q_table.pkl`, which training produces. Run training before testing —
> checkpoints are not committed.
