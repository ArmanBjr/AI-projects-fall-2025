"""Run the forward and backward planners on the flat-tyre problem.

Swap in BlockDomain/Block or LabRobotsDomain/LabRobotsProblem to plan in another domain.
"""

from Domains.TireDomain import TireDomain
from Problems.TireProblem import Tire
from Planners.ForwardPlanner import ForwardPlanner
from Planners.BackwardPlanner import BackwardPlanner

if __name__ == '__main__':
    problem = Tire(TireDomain())

    for planner_class in (ForwardPlanner, BackwardPlanner):
        plan = planner_class(problem).search()
        print(f'{planner_class.__name__}:')
        for step, action in enumerate(plan, start=1):
            print(f'  {step}. {action}')
        print()
