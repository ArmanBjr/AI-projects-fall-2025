#4021262131
#4021262459
from Solution import Solution
from Problem import Problem
from datetime import datetime
import heapq

class Search:
    @staticmethod
    def bfs(prb: Problem) -> Solution:
        start_time = datetime.now()
        queue = []
        state = prb.initState
        queue.append(state)
        max_counter = 200
        while len(queue) > 0 or max_counter > 0:
            max_counter -= 1
            state = queue.pop(0)
            neighbors = prb.successor(state)
            for c in neighbors:
                if prb.goal_test(c):
                    return Solution(c, prb, start_time)
                queue.append(c)
        return None
    
    @staticmethod
    def dfs(prb: Problem) -> Solution:
        start_time = datetime.now()
        stack = []
        state = prb.initState
        stack.append(state)
        visited = []
        # visited = {}
        visited.append(state)
        # visited[state.__hash__()] = 10
        while len(stack) > 0:
            state = stack.pop()
            neighbors = prb.successor(state)
            for c in neighbors:
                if prb.goal_test(c):
                    return Solution(c, prb, start_time)
                if c not in visited:
                    visited.append(c)
                    stack.append(c)
        return None
    
    @staticmethod
    def dfs_by_explore(prb: Problem) -> Solution:
        start_time = datetime.now()
        stack = []
        state = prb.initState
        stack.append(state)
        visited = {}
        visited[state.__hash__()] = 10
        while len(stack) > 0:
            state = stack.pop()
            neighbors = prb.successor(state)
            for c in neighbors:
                if prb.goal_test(c):
                    return Solution(c, prb, start_time)
                if c.__hash__() not in visited:
                    visited[c.__hash__()] = 10
                    stack.append(c)
        return None

    def DLS(prb: Problem, limit) -> Solution: # type: ignore
            start_time = datetime.now()
            stack = []
            state = prb.initState
            stack.append(state)
            visited = {}
            visited[state.__hash__()] = 10
            while len(stack) > 0:
                state = stack.pop()
                # if state.g_n > limit:
                #     break
                neighbors = prb.successor(state)
                for c in neighbors:
                    if prb.goal_test(c):
                        return Solution(c, prb, start_time)
                    if c.__hash__() not in visited:
                        visited[c.__hash__()] = 10
                        if not c.g_n > limit:
                            stack.append(c)
            return None

    @staticmethod
    def IDS(prb: Problem) -> Solution:
        max_limit = 100
        for L in range(max_limit + 1):
            Solution = Search.DLS(prb, L)
            if Solution != None:
                return Solution
            
    def UCS(prb: Problem) -> Solution:
        start_time = datetime.now()
        state = prb.initState
        pq = [(0, state)]
        max_counter = 200
        while len(pq) > 0 or max_counter > 0:
            cost, c = heapq.heappop(pq)
            if prb.goal_test(c):
                return Solution(c, prb, start_time)
            max_counter -= 1
            neighbors = prb.successor(state)
            for c in neighbors:
                if prb.goal_test(c):
                    return Solution(c, prb, start_time)
                heapq.heappush(pq, (c.g_n,c))
        return None
            

