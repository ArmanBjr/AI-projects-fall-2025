from CSP.Problem import Problem
from CSP.Variable import Variable
from CourseScheduler.Course import Course
from CourseScheduler.CourseConstraint import CourseConstraint
from CourseScheduler.AllDiffConstraint import AllDiffConstraint

class SchedulerProblem(Problem):
    def __init__(self):
        super().__init__([], [], "Scheduler Problem")
        """
        TODO:
        implementation guide:
        1. define domain
        2. define variables
        3. define constraints
        """ 
        c1 = Course("architecture", "farzam", 4)
        c2 = Course("automata", "Dr. Abrishami", 4)
        c3 = Course("pajohesh", "sedaghat", 4)
        c4 = Course("os", "allahbakhs", 5)
        c5 = Course("narm", "rasool", 5)
        c6 = Course("ai", "Dr. Abrishami", 5)
        c7 = Course("digital system", "farzam", 6)
        c8 = Course("micro", "sedaghat", 6)
        c9 = Course("special", "allahbakhs", 6)

        V11 = Variable[Course]([c1, c2, c3, c4, c5, c6, c7, c8, c9], 'Class1Time1')
        V12 = Variable[Course]([c1, c2, c3, c4, c5, c6, c7, c8, c9], 'Class1Time2')
        V13 = Variable[Course]([c1, c2, c3, c4, c5, c6, c7, c8, c9], 'Class1Time3')
        V21 = Variable[Course]([c1, c2, c3, c4, c5, c6, c7, c8, c9], 'Class2Time1')
        V22 = Variable[Course]([c1, c2, c3, c4, c5, c6, c7, c8, c9], 'Class2Time2')
        V23 = Variable[Course]([c1, c2, c3, c4, c5, c6, c7, c8, c9], 'Class2Time3')
        V31 = Variable[Course]([c1, c2, c3, c4, c5, c6, c7, c8, c9], 'Class3Time1')
        V32 = Variable[Course]([c1, c2, c3, c4, c5, c6, c7, c8, c9], 'Class3Time2')
        V33 = Variable[Course]([c1, c2, c3, c4, c5, c6, c7, c8, c9], 'Class3Time3')
    
        cons10 = AllDiffConstraint([V11, V12, V13, V21, V22, V23, V31, V32, V33])
        # cons2 = CourseConstraint([V11, V12])
        # cons3 = CourseConstraint([V11, V13]) 
        # cons4 = CourseConstraint([V12, V13])

        # cons5 = CourseConstraint([V21, V22])
        # cons6 = CourseConstraint([V21, V23])
        # cons7 = CourseConstraint([V22, V23])

        # cons8 = CourseConstraint([V31, V32])
        # cons9 = CourseConstraint([V31, V33])
        # cons10 = CourseConstraint([V32, V33])

        # time-1 column must be clash-free:
        cons1 = CourseConstraint([V11, V21])
        cons2 = CourseConstraint([V11, V31])
        cons3 = CourseConstraint([V21, V31])

        # time-2 column:
        cons4 = CourseConstraint([V12, V22])
        cons5 = CourseConstraint([V12, V32])
        cons6 = CourseConstraint([V22, V32])

        # time-3 column:
        cons7 = CourseConstraint([V13, V23])
        cons8 = CourseConstraint([V13, V33])
        cons9 = CourseConstraint([V23, V33])


        self.variables = [V11, V12, V13, V21, V22, V23, V31, V32, V33]
        self.constraints = [cons1, cons2, cons3, cons4, cons5, cons6, cons7, cons8, cons9, cons10]


    def print_assignments(self):
        for var in self.variables:
            if var.value is None:
                print(f"{var.name} is not assigned")
            else:
                c = var.value
                print(f"{var.name} -> {c.name} ({c.prof}, term {c.term})")
