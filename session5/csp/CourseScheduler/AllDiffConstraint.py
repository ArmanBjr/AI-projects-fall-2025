# CourseScheduler/AllDiffConstraint.py
from CSP.Constraint import Constraint

class AllDiffConstraint(Constraint):
    def is_satisfied(self) -> bool:
        # allow partial assignments; just ensure no duplicates among the assigned ones
        values = [x.value for x in self.variables if x.value is not None]
        return len(values) == len(set(values))
