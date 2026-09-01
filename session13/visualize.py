import time
import os
import sys
from tetris import MiniTetris

class Colors:
    RESET = "\033[0m"

    @staticmethod
    def supports_truecolor():
        if os.getenv("COLORTERM") in ("truecolor", "24bit"):
            return True
        if "WT_SESSION" in os.environ:
            return True
        if sys.platform != "win32":
            return True
        return False

    @staticmethod
    def rgb(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    if supports_truecolor():
        I_PIECE = rgb(0, 255, 255)       # Cyan
        Z_PIECE = rgb(255, 70, 70)       # Red
        H_PIECE = rgb(255, 215, 0)       # Gold
        EMPTY   = rgb(140, 140, 140)     # Neutral gray
        PREVIEW = rgb(50, 220, 120)      # Green
    else:
        I_PIECE = "\033[36m"
        Z_PIECE = "\033[31m"
        H_PIECE = "\033[33m"
        EMPTY   = "\033[37m"
        PREVIEW = "\033[32m"

    HEADER = "\033[35m"
    BOLD = "\033[1m"

    @staticmethod
    def colored(text, color):
        return f"{color}{text}{Colors.RESET}"


if not sys.stdout.isatty():
    Colors.I_PIECE = Colors.Z_PIECE = Colors.H_PIECE = ""
    Colors.EMPTY = Colors.PREVIEW = Colors.RESET = ""


class AgentVisualizer:
    def __init__(self, agent, delay=1.0):
        self.agent = agent
        self.delay = delay

    def get_q_values(self, state):
        q_values = {}

        for action in range(4):
            if (state, action) not in self.agent.transitions:
                q_values[action] = None
                continue

            q = 0.0
            trans_list = self.agent.transitions[(state, action)]
            prob = 1.0 / len(trans_list)

            for next_state, reward, done in trans_list:
                if done:
                    q += prob * reward
                else:
                    q += prob * (reward + self.agent.gamma * self.agent.U[next_state])

            q_values[action] = q

        return q_values

    def visualize_board(self, env, step_num, total_score):
        print("\n" + "=" * 70)
        print(f"STEP {step_num} | Score: {total_score}")
        print("=" * 70)

        piece_names = {
            1: "I (vertical)",
            2: "Z (Rhode Island Z)",
            3: "H (horizontal)"
        }

        piece_colors = {
            1: Colors.I_PIECE,
            2: Colors.Z_PIECE,
            3: Colors.H_PIECE
        }

        print(
            f"\n  Current: {Colors.colored('█', piece_colors.get(env.current_piece))} "
            f"{piece_names.get(env.current_piece)}"
        )
        print(
            f"  Next:    {Colors.colored('█', piece_colors.get(env.next_piece))} "
            f"{piece_names.get(env.next_piece)}"
        )

        print("\n  Board:")
        print("  ┌" + "─" * (env.width * 2 + 1) + "┐")

        for r in range(env.height):
            print("  │ ", end="")
            for c in range(env.width):
                cell = env.board[r, c]
                if cell == 2:
                    print(Colors.colored("█", Colors.I_PIECE), end=" ")
                elif cell == 3:
                    print(Colors.colored("█", Colors.Z_PIECE), end=" ")
                elif cell == 4:
                    print(Colors.colored("█", Colors.H_PIECE), end=" ")
                else:
                    print(Colors.colored("░", Colors.EMPTY), end=" ")
            print("│")

        print("  └" + "─" * (env.width * 2 + 1) + "┘")
        print("    " + " ".join(map(str, range(env.width))))

    def visualize_decision(self, state, q_values, chosen_action, valid_actions, piece_name):
        print(f"\n  Current Piece: {piece_name}")
        print(f"  Valid Actions: {valid_actions}")
        print("\n  Q-Values:")
        print("  " + "-" * 50)

        for a in range(4):
            q = q_values.get(a)
            if a not in valid_actions:
                label = "✗ Invalid"
                bar = ""
                val = "N/A"
            elif q is None:
                label = "? Unknown"
                bar = ""
                val = "—"
            else:
                label = "✓ Valid"
                norm = max(0, min(1, (q + 20) / 120))
                bar = "█" * int(norm * 20)
                val = f"{q:7.2f}"

            marker = "→" if a == chosen_action else " "
            print(f"  {marker} Col {a}: {bar:<20} {val:>8}  {label}")

        print("  " + "-" * 50)
        print(f"  ★ Agent chooses column {chosen_action}")

    def play_episode(self, max_steps=50):
        env = MiniTetris()
        state = env.reset()
        score = 0
        step = 0

        print("\n" + "=" * 70)
        print("STARTING NEW GAME")
        print("=" * 70)

        self.visualize_board(env, step, score)
        time.sleep(self.delay)

        while not env.game_over and step < max_steps:
            step += 1
            valid_actions = env.get_valid_actions()

            if not valid_actions:
                break

            if state in self.agent.policy and self.agent.policy[state] in valid_actions:
                action = self.agent.policy[state]
            else:
                q = self.get_q_values(state)
                valid_q = {a: q[a] for a in valid_actions if q[a] is not None}
                action = max(valid_q, key=valid_q.get) if valid_q else valid_actions[0]

            piece_name = {
                1: "I (vertical)",
                2: "Z",
                3: "H"
            }.get(state[-1], "Unknown")

            self.visualize_decision(state, self.get_q_values(state), action, valid_actions, piece_name)

            state, reward, done = env.step(action)
            score += reward

            print(f"\n  Reward: {reward:+.1f}")
            self.visualize_board(env, step, score)

            if done:
                print("\n" + "=" * 70)
                print("GAME OVER")
                print(f"Final Score: {score}")
                print("=" * 70)
                break

            time.sleep(self.delay)

        return score
