import random
from Solution import Solution
from Problem import Problem
from datetime import datetime
from queue import PriorityQueue
from State import State
#4021262459
#4021262131
class Search:
    @staticmethod
    def bfs(prb: Problem) -> Solution:
        start_time = datetime.now()
        queue = []
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop(0)
            neighbors = prb.successor(state)
            for c in neighbors:
                if prb.goal_test(c):
                    return Solution(c, prb, start_time)
                queue.append(c)
        return None

    @staticmethod
    def gbfs(prb: Problem) -> Solution:
        start = prb.initState
        start_time = datetime.now()
        Heap_1 = PriorityQueue()
        tie = 0
        Heap_1.put((start.h_n(), tie, start))
        while Heap_1:
            i, j, s = Heap_1.get()
            if prb.goal_test(s):
                return Solution(s, prb, start_time)
            for c in prb.successor(s):
                Heap_1.put((c.h_n(), tie, c))
                tie += 1
        return None

    @staticmethod
    def aStar(prb: Problem) -> Solution:
        start_time = datetime.now()
        start = prb.initState
        Heap_1 = PriorityQueue()
        tie = 0 # tie baraye vaghti bekar mire ke mosavi bashe!
        Heap_1.put((start.f_n(), start.g_n, tie, start))
        while Heap_1:
            i, j, m, s = Heap_1.get()
            if prb.goal_test(s):
                return Solution(s, prb, start_time)
            for c in prb.successor(s):
                Heap_1.put((c.f_n(), c.g_n, tie, c))
                tie += 1
        return None

    @staticmethod
    def ida(prb: Problem) -> Solution:
        start_time = datetime.now()
        start = prb.initState
        start_f = start.f_n()
        threshold = start_f
        while True:
            result = Search.ida_search(prb, start, threshold, start_time)
            if type(result) is Solution:
                return result
            else:
                threshold = result
                print(threshold)

    @staticmethod
    def ida_search(prb: Problem, state: State, threshold: int, start_time) -> Solution:
        stack = []
        stack.append(state)
        visited = []
        visited.append(state)
        Minimum = float('inf')
        while len(stack) > 0:
            s = stack.pop()
            neighbors = prb.successor(s)
            for c in neighbors:
                if prb.goal_test(c):
                    return Solution(c, prb, start_time)
                if c.f_n() <= threshold:
                    visited.append(c)
                    stack.append(c)
                else:
                    Minimum = min(Minimum, c.f_n())
        return Minimum

    @staticmethod
    def rbfs(prb: Problem) -> Solution:
        start_time = datetime.now()
        start = prb.initState
        
        node_fvals = {}
        node_fvals[start.board.hash()] = start.f_n()

        Search.rbfs_search(prb, start, float('inf'), start_time)
        pass
        
    @staticmethod
    def rbfs_search(prb: Problem, state: State, f_limit: int, start_time) -> Solution:
        if prb.goal_test(state):
            return Solution(state, prb, start_time)
        children = []
        for ch in prb.successor(state):
            f = ch.f_n()
            children.append([ch, f])

        if not children:
            return None
        while True:
            children.sort(key=lambda x : x[1])
            best_s, best_f = children[0]

            if best_f > state.__f_limit:
                return best_f
            alternative_path = children[1][1] if len(children) > 1 else float('inf')
        
            result = Search.rbfs_search(prb, ch, ch.__f_limit, start_time)
            if result is not None:
                return result
            children[0][1] = best_f            
            # edame nemidim dige
    def hill_climbing(prb: Problem) -> Solution:
        start_time = datetime.now()
        current = prb.initState
        def val(s: State):
            return -float(s.h_n())
        
        while True:
            if prb.goal_test(current):
                return Solution(current, prb, start_time)
            neighbors = prb.successor(current)
            if not neighbors:
                return Solution(current, prb, start_time)
            best = max(neighbors, key=val)
            if val(best) <= val(current):
                return Solution(current, prb, start_time)
            
            current = best
    
    def hill_climbing(prb: Problem, state: State) -> Solution:
        start_time = datetime.now()
        if not state:
            current = prb.initState
        def val(s: State):
            return -float(s.h_n())
        
        while True:
            if prb.goal_test(current):
                return Solution(current, prb, start_time)
            neighbors = prb.successor(current)
            if not neighbors:
                return Solution(current, prb, start_time)
            best = max(neighbors, key=val)
            if val(best) <= val(current):
                return Solution(current, prb, start_time) 
            current = best

    def random_restart(prb: Problem) -> Solution:
        start_time = datetime.now()
        def val(s: State):
            return -float(s.h_n)
        best_solution = None
        best_val = None
        restarts = 1000
        s0 = prb.initState
        sol0 = Search.hill_climbing(prb, s0)
        best_solution, best_val = sol0, val(sol0.state)

        for i in range(restarts):
            neis = prb.successor(s0)
            seed = random.choice(neis)
            sol = Search.hill_climbing(prb, seed) 
            v = val(sol.state)
            if v > best_val:
                best_solution = sol
                best_val = v
        return best_val
    
    def stoch_hill(prb: Problem) -> Solution:
        start_time = datetime.now()
        state = prb.initState()

        def val(s: State):
            return -float(s.h_n())

        while True:
            if prb.goal_test(state):
                return Solution(state, prb, start_time)

            neighbor = prb.successor(state)
            if not neighbor:
                return Solution(state , prb, start_time)
            
            values = [val(n) for n in neighbor]
            max_val = max(values)

            if max_val <= val(state):
                return Solution(state, prb, start_time)
            
            total = sum(v for v in values)
            probs = [(v - min(values) + 1e-6) / total for v in values]
            next_state = random.choice(neighbor, weights = probs, k = 1)[0]
            state = next_state

        return Solution(state, prb, start_time)

