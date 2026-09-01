from Domains.TireDomain import TireDomain
from Domains.BlockWorld import BlockDomain
from Problems.TireProblem import Tire
from Problems.block import Block
from Planners.ForwardPlanner import ForwardPlanner
from Planners.BackwardPlanner import BackwardPlanner
from Domains.LabRobotsDomain import LabRobotsDomain
from Problems.LabRobotsProblem import LabRobotsProblem


# planner1 = BackwardPlanner(LabRobotsProblem(LabRobotsDomain()))

# planner = ForwardPlanner(LabRobotsProblem(LabRobotsDomain()))
# # planner = ForwardPlanner(Tire(TireDomain()))
# print(planner1.search())

# from Planners.GraphPlanPlanner import GraphPlanPlanner
# from Domains.LabRobotsDomain import LabRobotsDomain
# from Problems.LabRobotsProblem import LabRobotsProblem

# planner = GraphPlanPlanner(LabRobotsProblem(LabRobotsDomain()))
# print(planner.search())

from Domains.TireDomain import TireDomain
from Problems.TireProblem import Tire
from Planners.GraphPlanPlanner import GraphPlanPlanner

planner = GraphPlanPlanner(Tire(TireDomain()), max_levels=100000)
print(planner.search())
