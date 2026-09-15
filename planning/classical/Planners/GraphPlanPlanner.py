# Planners/GraphPlanPlanner.py

from Model.Predicate import Predicate
from Planners.Planner import Planner
from Planners.PlanningGraph import PlanningGraph


class GraphPlanPlanner(Planner):
    """
    پیاده‌سازی الگوریتم GRAPHPLAN مطابق شبه‌کد کتاب:
        graph ← INITIAL-PLANNING-GRAPH(problem)
        goals ← CONJUNCTS(problem.GOAL)
        nogoods ← {}
        for t = 0 to ∞:
            if goals all non-mutex in S_t of graph:
                solution ← EXTRACT-SOLUTION(...)
                if solution ≠ failure: return solution
            if graph and nogoods have both leveled off: return failure
            graph ← EXPAND-GRAPH(graph, problem)
    """

    def __init__(self, problem, max_levels: int = 20):
        super().__init__(problem)
        self.graph = PlanningGraph(problem)
        self.max_levels = max_levels

    # ---------------------------------------------------------
    # GRAPHPLAN(problem) → solution or failure
    # ---------------------------------------------------------
    def search(self):
        goals = set(self.problem.goal_state.literals)
        # nogoods: مجموعه‌ای از (level, frozenset(goals)) که شکست خورده‌اند
        nogoods: set[tuple[int, frozenset[Predicate]]] = set()

        t = 0
        last_nogoods_size = -1

        while True:
            # if goals all non-mutex in S_t of graph then ...
            if self.graph.goals_non_mutex(goals, t):
                solution = self._extract_solution(goals, t, nogoods)
                if solution is not None:  # solution ≠ failure
                    return solution

            # if graph and nogoods have both leveled off then return failure
            if (
                self.graph.leveled_off()
                and len(nogoods) == last_nogoods_size
            ):
                # failure → اینجا [] برمی‌گردونیم
                return []

            # به انتهای max_levels نرسیدیم؟ اگر رسیدیم، شکست.
            if t >= self.max_levels:
                return []

            # graph ← EXPAND-GRAPH(graph, problem)
            last_nogoods_size = len(nogoods)
            self.graph.expand_one_level()
            t += 1

    # ---------------------------------------------------------
    # EXTRACT-SOLUTION(graph, goals, t, nogoods)
    # (بازگشتی، بر اساس الگوریتم استاندارد GraphPlan)
    # ---------------------------------------------------------
    def _extract_solution(
        self,
        goals: set[Predicate],
        level: int,
        nogoods: set[tuple[int, frozenset[Predicate]]],
    ):
        key = (level, frozenset(goals))
        if key in nogoods:
            return None

        # اگر سطح 0 است، باید goals زیرمجموعه‌ی S_0 باشند
        if level == 0:
            s0 = self.graph.literal_levels[0]
            if goals.issubset(s0):
                return []  # قبل از S0 هیچ اکشنی نداریم
            else:
                nogoods.add(key)
                return None

        # اگر goals اصلاً در این سطح حاضر نیستند، شکست
        if not self.graph.goals_non_mutex(goals, level):
            nogoods.add(key)
            return None

        actions_level = self.graph.action_levels[level - 1]
        prev_literals = self.graph.literal_levels[level - 1]
        action_mutex = self.graph.action_mutex[level - 1]

        # producers[g] = لیست اکشن‌هایی که g را تولید می‌کنند
        producers: dict[Predicate, list] = {}
        for g in goals:
            producers[g] = [a for a in actions_level if g in a.add_list]

        goals_list = list(goals)

        # ---------------- انتخاب مجموعه اکشن‌ها برای این سطح (backtracking) ----------------
        def backtrack(i: int, chosen_actions: set):
            # همه‌ی goalها را بررسی کردیم → یک ست اکشن پیدا شده
            if i == len(goals_list):
                return chosen_actions.copy()

            g = goals_list[i]

            # اگر g همین الان توسط اکشن‌های انتخاب‌شده یا persistence ساپورت است
            if self._goal_supported_by_chosen(g, chosen_actions, prev_literals, goals):
                res = backtrack(i + 1, chosen_actions)
                if res is not None:
                    return res

            # در غیر این صورت، باید اکشنی که g را تولید کند انتخاب کنیم
            candidate_actions = producers.get(g, [])
            if not candidate_actions:
                return None  # هیچ اکشنی g را تولید نمی‌کند

            for a in candidate_actions:
                # اگر از قبل انتخاب شده، برو goal بعدی
                if a in chosen_actions:
                    res = backtrack(i + 1, chosen_actions)
                    if res is not None:
                        return res
                    continue

                # اکشن با یکی از اکشن‌های انتخاب‌شده mutex است؟
                conflict = False
                for other in chosen_actions:
                    if frozenset({a, other}) in action_mutex:
                        conflict = True
                        break
                if conflict:
                    continue

                # این اکشن نباید هیچ کدام از goalهای سطح t را delete کند
                if a.delete_list & goals:
                    continue

                chosen_actions.add(a)
                res = backtrack(i + 1, chosen_actions)
                if res is not None:
                    return res
                chosen_actions.remove(a)

            return None

        selected_actions = backtrack(0, set())
        if selected_actions is None:
            nogoods.add(key)
            return None

        # ---------------- regression برای رفتن به سطح قبلی ----------------
        new_goals = set(goals)
        add_union = set()
        pre_union = set()

        for a in selected_actions:
            add_union |= a.add_list
            pre_union |= a.positive_preconditions

        new_goals = (new_goals - add_union) | pre_union

        subplan = self._extract_solution(new_goals, level - 1, nogoods)
        if subplan is None:
            nogoods.add(key)
            return None

        # اکشن‌های این سطح را به ترتیب نام، به انتهای plan اضافه می‌کنیم
        ordered_actions = sorted(selected_actions, key=lambda ac: ac.action_name)
        return subplan + [a.action_name for a in ordered_actions]

    # ---------------- توابع کمکی ----------------
    def _goal_supported_by_chosen(
        self,
        g: Predicate,
        chosen_actions: set,
        prev_literals: set[Predicate],
        goals_at_level: set[Predicate],
    ) -> bool:
        """
        g توسط اکشن‌های انتخاب‌شده یا persistence ساپورت می‌شود اگر:
        - یکی از اکشن‌ها g را add کند؛ یا
        - g در S_{t-1} باشد و هیچ اکشنی آن را delete نکند.
        """
        # توسط یکی از اکشن‌ها تولید می‌شود؟
        for a in chosen_actions:
            if g in a.add_list:
                return True

        # یا با persistence (no-op ضمنی)
        if g in prev_literals:
            for a in chosen_actions:
                if g in a.delete_list:
                    return False
            return True

        return False
