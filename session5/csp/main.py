from CSP.Solver import Solver
from States.StatesProblem import StatesProblem
from CourseScheduler.SchedulerProblem import SchedulerProblem


if __name__ == '__main__':

    SchedulerP = SchedulerProblem()
    s = Solver(SchedulerP)
    s.solve()
    SchedulerP.print_assignments()
    