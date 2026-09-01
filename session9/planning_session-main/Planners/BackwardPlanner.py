from queue import Queue

from Model.State import State
from Planners.Planner import Planner

"""
result is a list that stores the sequence of actions needed to reach the goal state, in case the planner finds a solution.

frontier is a queue data structure that states that need to be expanded. It follows the First-In-First-Out (FIFO) rule, meaning that the first state that was added to the queue will be the first one to be explored.

visited is a set that stores all the states that have already been visited during the search process. If a state has already been visited, it will not be added to either the frontier or all_states again. This helps to prevent the algorithm from revisiting the same states multiple times and getting stuck in a loop

"""


class BackwardPlanner(Planner):
    def __init__(self, problem):
        super().__init__(problem)

    from queue import Queue

from Model.State import State
from Planners.Planner import Planner


class BackwardPlanner(Planner):
    def __init__(self, problem):
        super().__init__(problem)

    def search(self):
        frontier = Queue()
        visited = set()

        initial = self.problem.initial_state
        goal = self.problem.goal_state

        # اگر initial خودش goal را ارضا کند، برنامه خالی است
        if initial.goal_test(goal):
            return []

        # گراف regression از خود goal شروع می‌شود
        frontier.put(goal)
        visited.add(goal)

        while not frontier.empty():
            current_state = frontier.get()

            # تولید predecessorها با regression
            predecessor_states = self.predecessor(current_state)

            for predecessor_state in predecessor_states:
                # اگر این goal جدید با initial سازگار/کافی باشد، برنامه را بساز
                if predecessor_state.initial_test(initial):
                    return predecessor_state.build_solution()

                if predecessor_state not in visited:
                    frontier.put(predecessor_state)
                    visited.add(predecessor_state)

        # اگر هیچ راه‌حلی پیدا نشد
        return []


    def predecessor(self, current_state: State) -> list[State]:
        result = []
        # don't forget to set parent
        for action in self.problem.domain.actions:
            if action.is_relevant(current_state):
                new_state = action.regress(current_state)
                new_state.parent = current_state
                result.append(new_state)

        return result

