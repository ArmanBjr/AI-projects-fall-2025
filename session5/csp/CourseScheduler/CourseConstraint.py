# CourseScheduler/CourseConstraint.py
from CSP.Constraint import Constraint

class CourseConstraint(Constraint):
    def is_satisfied(self) -> bool:
        assigned = [v for v in self.variables if v.value is not None]
        if len(assigned) < 2:
            return True  # nothing to compare yet
        a, b = assigned[0].value, assigned[1].value
        # same professor or same term cannot be at the same time slot
        return not (a.prof == b.prof or a.term == b.term)
