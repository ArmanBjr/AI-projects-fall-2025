# Planners/PlanningGraph.py

from Model.Predicate import Predicate
from Model.State import State
from Problems.Problem import Problem
from Model.Action import Action


class PlanningGraph:
    """
    Planning Graph ساده بر پایه STRIPS:
    - فقط literalهای مثبت داریم (همون state.literals فعلی).
    - لایه‌ها:
        S_t : مجموعه‌ی literalها
        A_t : مجموعه‌ی actionهای قابل اجرا از S_t
    - action-mutex را حساب می‌کنیم (inconsistent effects + interference).
    - literal-mutex را فعلاً خالی می‌گذاریم (برای سادگی).
    """

    def __init__(self, problem: Problem):
        self.problem = problem

        # S_t و A_t
        self.literal_levels: list[set[Predicate]] = []
        self.action_levels: list[set[Action]] = []

        # mutex ها
        self.literal_mutex: list[set[frozenset[Predicate]]] = []
        self.action_mutex: list[set[frozenset[Action]]] = []

        # S_0
        init_literals = set(problem.initial_state.literals)
        self.literal_levels.append(init_literals)
        self.literal_mutex.append(set())  # فعلاً چیزی نداریم

    # ---------------------------------------------------------
    # EXPAND-GRAPH(graph, problem)
    # ---------------------------------------------------------
    def expand_one_level(self) -> None:
        """
        از آخرین سطح literal:
        1) A_t را می‌سازد (اکشن‌های قابل اجرا)
        2) action-mutex را حساب می‌کند
        3) S_{t+1} را می‌سازد (literals جدید)
        4) literal-mutex را فعلاً خالی می‌گذاریم
        """
        current_literals = self.literal_levels[-1]
        temp_state = State("level", list(current_literals))

        # 1) ساختن A_t
        actions = set()
        for action in self.problem.domain.actions:
            if action.is_applicable(temp_state):
                actions.add(action)
        self.action_levels.append(actions)

        # 2) محاسبه‌ی action-mutex (ساده‌شده)
        mutex_pairs: set[frozenset[Action]] = set()
        actions_list = list(actions)
        n = len(actions_list)
        for i in range(n):
            for j in range(i + 1, n):
                a = actions_list[i]
                b = actions_list[j]
                if self._actions_mutex(a, b):
                    mutex_pairs.add(frozenset({a, b}))
        self.action_mutex.append(mutex_pairs)

        # 3) ساختن S_{t+1}
        new_literals = set(current_literals)  # persistence ضمنی
        for a in actions:
            new_literals |= a.add_list
        self.literal_levels.append(new_literals)

        # 4) literal-mutex خالی
        self.literal_mutex.append(set())

    def _actions_mutex(self, a: Action, b: Action) -> bool:
        """
        دو اکشن mutex هستند اگر:
        - inconsistent effects: یکی literalی را اضافه کند که دیگری حذف می‌کند
        - interference: اثرات یکی precondition دیگری را خراب کند
        (برای سادگی competing needs را حساب نمی‌کنیم)
        """
        # inconsistent effects
        if (a.add_list & b.delete_list) or (b.add_list & a.delete_list):
            return True

        # interference با preconditions
        if (a.delete_list & a.positive_preconditions) or (
            b.delete_list & b.positive_preconditions
        ):
            return True

        if (a.delete_list & b.positive_preconditions) or (
            b.delete_list & a.positive_preconditions
        ):
            return True

        return False

    # ---------------------------------------------------------
    # ابزار برای GraphPlan
    # ---------------------------------------------------------
    def goals_non_mutex(self, goals: set[Predicate], level: int) -> bool:
        """
        چک می‌کند goals ⊆ S_level و (در این نسخه‌ی ساده) literal-mutex ندارند.
        """
        if level >= len(self.literal_levels):
            return False

        literals = self.literal_levels[level]
        if not goals.issubset(literals):
            return False

        # اگر literal-mutex واقعی می‌ساختیم، اینجا چک می‌کردیم.
        return True

    def leveled_off(self) -> bool:
        """
        leveled off وقتی است که دو سطح آخر literal دقیقاً برابر باشند.
        """
        if len(self.literal_levels) < 2:
            return False
        return self.literal_levels[-1] == self.literal_levels[-2]
