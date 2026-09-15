import os
import subprocess
import time
from collections import deque
from copy import deepcopy
from typing import Optional

from CSP.Problem import Problem
from CSP.Variable import Variable


class Solver:

    def __init__(self, problem: Problem):
        """
        Initializes the Solver object with the given problem instance and optional parameters.

        Args:
            problem (Problem): The problem instance to be solved.
        """
        self.problem = problem
        self.back_up = deque()

    def is_finished(self) -> bool:
        """
        Determines if the problem has been solved.

        Returns:
            bool: True if the problem has been solved, False otherwise.
        """
        return all([x.is_satisfied() for x in self.problem.constraints]) and len(
            self.problem.get_unassigned_variables()) == 0

    def solve(self):
        """
        Solves the problem instance using the backtracking algorithm with optional heuristics.
        """
        start = time.time()
        result = self.backtracking()
        end = time.time()
        time_elapsed = (end - start) * 1000
        if result:
            print(f'Solved after {time_elapsed} ms')
        else:
            print(f'Failed to solve after {time_elapsed} ms')

    def backtracking(self) -> bool:
        """
        Backtracking with MRV (variable choice), LCV (value order),
        and Forward Checking for inference.
        """
        if self.is_finished():
            return True

        var = self.mrv()
        if var is None:
            return False

        for value in self.lcv(var):
            self.save_domain(self.problem.variables)
            var.value = value
            if self.is_consistent(var) and self.forward_check(var):
                if self.backtracking():
                    return True
            var.value = None
            self.load_domain(self.problem)
        return False


    def forward_check(self, var: Variable) -> bool:
        """
        Implements the Forward Checking algorithm.
        
        """
        constraints = self.problem.get_constraints(var)

        for neighbor in var.neighbors:
            if neighbor.has_value:
                continue
            tmp = neighbor.domain.copy()
            for value in tmp:
                neighbor.value = value
                for constraint in constraints:
                    if neighbor in constraint.variables:
                        if not constraint.is_satisfied():
                            tmp.remove(value)
                            break                
            neighbor.value = None
            if len(tmp) == 0:
                return False
            else:
                neighbor.domain=tmp              
        return True
                        

    def mrv(self) -> Optional[Variable]:
        """
        Implements the Minimum Remaining Values heuristic.

        Returns:
            Optional[Variable]: The variable with the smallest domain or None if all variables have been assigned.
        """
        #TODO: implement mrv

        unassigned = self.problem.get_unassigned_variables()
        if not unassigned:
            return None
        return min(unassigned, key=lambda v: len(v.domain))
        pass

    def is_consistent(self, var: Variable) -> bool:
        """
        Determines ifthe given variable is consistent with all constraints.

        Args:
            var (Variable): The variable to be checked for consistency.

        Returns:
            bool: True if the variable is consistent with all constraints, False otherwise.
        """
        return all(constraint.is_satisfied() for constraint in self.problem.constraints if var in constraint.variables)

    def lcv(self, var: Variable):
        """
        Least Constraining Value: order var's domain values by how few
        options they eliminate from neighbors' domains (ascending).
        """
        # constraints that involve 'var' (we'll only check those)
        var_constraints = self.problem.get_constraints(var)

        def eliminated_count(vx) -> int:
            # Temporarily assign var = vx while we "probe" neighbors
            old_v = var.value
            var.value = vx
            try:
                cnt = 0
                for nb in var.neighbors:
                    if nb.has_value:
                        continue
                    for vy in nb.domain:
                        # check only constraints that include BOTH var and nb
                        ok = True
                        old_nb = nb.value
                        nb.value = vy
                        try:
                            for c in var_constraints:
                                if nb in c.variables and not c.is_satisfied():
                                    ok = False
                                    break
                        finally:
                            nb.value = old_nb
                        if not ok:
                            cnt += 1
                return cnt
            finally:
                var.value = old_v

        # Return a fresh, ordered list (do not mutate var.domain)
        return sorted(list(var.domain), key=eliminated_count)

    
    def save_domain(self, vars: list[Variable]):
        self.back_up.append([var.domain.copy() for var in vars])
    
    def load_domain(self, problem: Problem):
        domains = self.back_up.pop()
        for i in range(len(problem.variables)):
            problem.variables[i].domain = domains[i]
