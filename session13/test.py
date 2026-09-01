import numpy as np
from copy import deepcopy

from mdp import MDP
from tetris import MiniTetris

def set_env_to_state(env: MiniTetris, heights, piece_type: int):
    """
    heights: لیست/تاپل 4تایی مثل [4,4,4,3]
    piece_type: 3 یعنی H-piece (زرد افقی)
    """
    env.board = np.zeros((env.height, env.width), dtype=int)

    # هر ستون را از پایین پر می‌کنیم تا ارتفاع دلخواه بسازیم
    for col, h in enumerate(heights):
        if h <= 0:
            continue
        start_row = env.height - h  # ردیفی که از آن به بعد پر می‌شود
        env.board[start_row:, col] = 4  # هر عدد >0 فرقی ندارد (بلاک)

    env.current_piece = piece_type
    env.next_piece = env._generate_piece()  # هرچی
    env.score = 0
    env.game_over = False

    return env.get_state()

def get_q_from_empirical_transitions(agent: MDP, state, action):
    """
    Q(s,a) = average over observed transitions:
      if done: reward
      else: reward + gamma * U[s']
    """
    if (state, action) not in agent.transitions:
        return None

    trans_list = agent.transitions[(state, action)]
    n = len(trans_list)
    if n == 0:
        return None

    prob = 1.0 / n
    q = 0.0
    for s_next, r, done in trans_list:
        if done:
            q += prob * r
        else:
            q += prob * (r + agent.gamma * agent.U[s_next])
    return q

def choose_action_by_q(agent: MDP, state, valid_actions):
    qvals = {}
    for a in valid_actions:
        qvals[a] = get_q_from_empirical_transitions(agent, state, a)

    # فقط اکشن‌هایی که Q معلوم دارند
    known = {a: q for a, q in qvals.items() if q is not None}
    if not known:
        return None, qvals  # هیچ دیتایی نداریم

    best_a = max(known, key=known.get)
    return best_a, qvals

def main():
    # ----------- 1) ساخت env و جمع کردن transitions یکسان -----------
    env = MiniTetris()
    base_agent = MDP(env, gamma=0.9, theta=1e-6)

    print("Collecting experience...")
    base_agent.collect_experience(num_episodes=5000)
    transitions = deepcopy(base_agent.transitions)  # ثابت نگه می‌داریم

    # ----------- 2) ساخت state هدف -----------
    target_heights = [4, 4, 4, 3]
    target_piece = 3  # H-piece (زرد افقی)
    target_state = tuple(target_heights + [target_piece])

    # محیط را دقیقاً روی همان state می‌گذاریم تا valid_actions واقعی را بگیریم
    set_env_to_state(env, target_heights, target_piece)
    valid_actions = env.get_valid_actions()

    print("\nTarget state =", target_state)
    print("Valid actions at this state =", valid_actions)

    # ----------- 3) Agent با gamma=0.0 -----------
    agent_g0 = MDP(env, gamma=0.0, theta=1e-6)
    agent_g0.transitions = deepcopy(transitions)

    print("\nTraining agent with gamma = 0.0 (Value Iteration)...")
    agent_g0.value_iteration(max_iterations=10000)

    best_a_g0, qvals_g0 = choose_action_by_q(agent_g0, target_state, valid_actions)

    print("\n[gamma=0.0] Q-values (only valid actions):")
    for a in valid_actions:
        print(f"  action {a}: {qvals_g0[a]}")
    print("[gamma=0.0] chosen action =", best_a_g0)

    # ----------- 4) Agent با gamma=0.9 -----------
    agent_g09 = MDP(env, gamma=0.9, theta=1e-6)
    agent_g09.transitions = deepcopy(transitions)

    print("\nTraining agent with gamma = 0.9 (Value Iteration)...")
    agent_g09.value_iteration(max_iterations=10000)

    best_a_g09, qvals_g09 = choose_action_by_q(agent_g09, target_state, valid_actions)

    print("\n[gamma=0.9] Q-values (only valid actions):")
    for a in valid_actions:
        print(f"  action {a}: {qvals_g09[a]}")
    print("[gamma=0.9] chosen action =", best_a_g09)

    # ----------- 5) جمع‌بندی مقایسه -----------
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("Target state:", target_state)
    print("Valid actions:", valid_actions)
    print("gamma=0.0 chosen:", best_a_g0)
    print("gamma=0.9 chosen:", best_a_g09)

    if best_a_g0 is None or best_a_g09 is None:
        print("\n⚠️ Note: At least one agent had no empirical transition data for this state.")
        print("Try increasing num_episodes to collect more transitions, e.g. 50_000 or 100_000.")

if __name__ == "__main__":
    main()
import numpy as np
from collections import Counter
from copy import deepcopy

from tetris import MiniTetris

# -----------------------------
# ابزار ساخت env در یک state خاص
# -----------------------------
def set_env_to_state(env: MiniTetris, heights, piece_type: int, next_piece=None):
    """
    heights: مثل [4,4,4,3]
    piece_type: 1=I, 2=Z, 3=H (زرد افقی)
    next_piece: اگر None باشد رندوم می‌گذاریم
    """
    env.board = np.zeros((env.height, env.width), dtype=int)

    # ستون‌ها را از پایین پر می‌کنیم تا ارتفاع دلخواه ساخته شود
    for col, h in enumerate(heights):
        if h <= 0:
            continue
        start_row = env.height - h
        env.board[start_row:, col] = 4  # هر عدد مثبت برای "پر بودن" کافی است

    env.current_piece = piece_type
    env.next_piece = env._generate_piece() if next_piece is None else next_piece
    env.score = 0
    env.game_over = False

    return env.get_state()

def snapshot_env(env: MiniTetris):
    """یک snapshot ساده از env برای برگشت به همان حالت"""
    return {
        "board": env.board.copy(),
        "current_piece": int(env.current_piece),
        "next_piece": int(env.next_piece),
        "score": float(env.score),
        "game_over": bool(env.game_over),
        "width": env.width,
        "height": env.height,
    }

def restore_env(env: MiniTetris, snap):
    env.board = snap["board"].copy()
    env.current_piece = snap["current_piece"]
    env.next_piece = snap["next_piece"]
    env.score = snap["score"]
    env.game_over = snap["game_over"]
    return env

# -----------------------------
# Rollout: از یک env شروع می‌کنیم و چند قدم بازی را ادامه می‌دهیم
# -----------------------------
def rollout_return(env: MiniTetris, gamma: float, horizon: int = 40):
    """
    با یک policy ساده (random-valid) تا horizon قدم جلو می‌رود
    و return تنزیل‌شده را حساب می‌کند.
    """
    G = 0.0
    discount = 1.0
    steps = 0

    while (not env.game_over) and (steps < horizon):
        valid = env.get_valid_actions()
        if not valid:
            break
        a = np.random.choice(valid)
        _, r, done = env.step(a)

        G += discount * r
        discount *= gamma

        steps += 1
        if done:
            break

    return G

# -----------------------------
# انتخاب اکشن با Monte Carlo:
# برای هر اکشن معتبر، چند rollout انجام می‌دهیم و میانگین return را می‌گیریم
# -----------------------------
def mc_choose_action_for_state(base_env: MiniTetris, heights, piece_type,
                              gamma: float,
                              rollouts_per_action: int = 50,
                              horizon: int = 40):
    """
    بر اساس MC rollouts، اکشن بهتر را انتخاب می‌کند.
    خروجی:
      chosen_action, q_estimates, valid_actions
    """
    # env را روی state تنظیم می‌کنیم
    env = base_env
    set_env_to_state(env, heights, piece_type)

    valid_actions = env.get_valid_actions()
    if not valid_actions:
        return None, {}, []

    # snapshot برای اینکه هر بار دقیقاً از همان state شروع کنیم
    snap = snapshot_env(env)

    q_est = {}
    for a in valid_actions:
        returns = []
        for _ in range(rollouts_per_action):
            # برگشت به state پایه
            restore_env(env, snap)

            # اکشن اول را اعمال می‌کنیم
            _, r1, done1 = env.step(a)

            # return = r1 + gamma * future
            if done1:
                G = r1
            else:
                G = r1 + (gamma * rollout_return(env, gamma=gamma, horizon=horizon-1))

            returns.append(G)

        q_est[a] = float(np.mean(returns))

    chosen = max(q_est, key=q_est.get)
    return chosen, q_est, valid_actions

# -----------------------------
# تست چندباره روی یک state برای دیدن "اکشن پرتکرار"
# -----------------------------
def repeated_choice_stats(heights, piece_type,
                          gamma: float,
                          n_trials: int = 200,
                          rollouts_per_action: int = 30,
                          horizon: int = 30,
                          seed: int = 0):
    """
    n_trials بار تصمیم می‌گیرد و می‌گوید پرتکرارترین action کدام است.
    """
    np.random.seed(seed)
    env = MiniTetris()

    counts = Counter()
    last_q = None
    valid_actions = None

    for _ in range(n_trials):
        chosen, q_est, valid = mc_choose_action_for_state(
            env, heights, piece_type,
            gamma=gamma,
            rollouts_per_action=rollouts_per_action,
            horizon=horizon
        )
        if chosen is not None:
            counts[chosen] += 1
            last_q = q_est
            valid_actions = valid

    return counts, last_q, valid_actions

# -----------------------------
# main: چند state را تست می‌کنیم + حالت خاص 4,4,4,3
# -----------------------------
def main():
    # چند حالت نمونه (همه با H-piece=3 برای همسانی)
    test_states = [
        ([0, 0, 0, 0], 3),
        ([2, 2, 2, 2], 3),
        ([3, 3, 3, 2], 3),
        ([4, 4, 4, 3], 3),  # همون حالت مورد سؤال
        ([5, 5, 4, 5], 3),
    ]

    # پارامترهای تکرار/رول‌اوت (می‌تونی زیادترشون کنی برای دقت بیشتر)
    n_trials = 200
    rollouts_per_action = 40
    horizon = 35

    # دو گاما
    gammas = [0.0, 0.9]

    print("=" * 80)
    print("MC ACTION CHOICE - MULTI STATE TEST")
    print("=" * 80)

    for heights, piece in test_states:
        state_str = f"state={tuple(heights + [piece])} (piece={piece})"
        print("\n" + "-" * 80)
        print(state_str)

        for g in gammas:
            counts, last_q, valid = repeated_choice_stats(
                heights, piece,
                gamma=g,
                n_trials=n_trials,
                rollouts_per_action=rollouts_per_action,
                horizon=horizon,
                seed=42  # ثابت برای مقایسه
            )

            if not counts:
                print(f"  gamma={g}: no valid choices observed")
                continue

            most_common_action, freq = counts.most_common(1)[0]
            print(f"\n  gamma={g}")
            print(f"  valid_actions = {valid}")
            print(f"  counts        = {dict(counts)}")
            print(f"  most_common   = action {most_common_action}  (freq {freq}/{n_trials})")

            # چاپ آخرین Q-estimate ها (میانگین MC) برای insight
            if last_q is not None:
                q_sorted = sorted(last_q.items(), key=lambda x: x[0])
                print("  last Q_estimates:")
                for a, q in q_sorted:
                    print(f"    action {a}: {q:.3f}")

    # ---- بخش ویژه برای 4,4,4,3 ----
    print("\n" + "=" * 80)
    print("SPECIAL ANALYSIS FOR (4,4,4,3, H-piece)")
    print("=" * 80)

    heights = [4, 4, 4, 3]
    piece = 3  # H piece
    for g in gammas:
        counts, last_q, valid = repeated_choice_stats(
            heights, piece,
            gamma=g,
            n_trials=400,                 # اینجا بیشتر می‌کنیم تا نتیجه قابل اتکا تر بشه
            rollouts_per_action=60,
            horizon=40,
            seed=123
        )

        most_common_action, freq = counts.most_common(1)[0]
        print(f"\nFor gamma={g}:")
        print(f"  valid_actions = {valid}")
        print(f"  counts        = {dict(counts)}")
        print(f"  most_common   = action {most_common_action}  (freq {freq}/400)")

        if last_q is not None:
            print("  Q_estimates (last trial):")
            for a in sorted(last_q.keys()):
                print(f"    action {a}: {last_q[a]:.3f}")

    print("\nDone.")

if __name__ == "__main__":
    main()
