from collections import deque

def bfs(start, goal, neighbors):
    queue = deque([[start]])  # each element = path
    visited = set([start])
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path
        for nxt in neighbors(node):
            if nxt not in visited:
                visited.add(nxt)
                queue.append(path + [nxt])
    return None

def dfs(start, goal, neighbors):
    stack = [[start]]
    visited = set([start])
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == goal:
            return path
        for nxt in neighbors(node):
            if nxt not in visited:
                visited.add(nxt)
                stack.append(path + [nxt])
    return None

import heapq

def ucs(start, goal, neighbors):
    pq = [(0, [start])]  # (cost, path)
    visited = {}
    while pq:
        cost, path = heapq.heappop(pq)
        node = path[-1]
        if node == goal:
            return path, cost
        if node in visited and visited[node] <= cost:
            continue
        visited[node] = cost
        for nxt, edge_cost in neighbors(node):
            heapq.heappush(pq, (cost + edge_cost, path + [nxt]))
    return None

CUT_OFF = object()
FAILURE = None

def depth_limited_search(start, goal_test, neighbors, limit):
    """
    start: start state
    goal_test: fn(state) -> bool
    neighbors: fn(state) -> iterable of next states
    limit: max depth allowed (root at depth 0)
    returns: path (list of states), or CUT_OFF, or FAILURE
    """
    def recursive_dls(node, path, depth):
        if goal_test(node):
            return path
        if depth == limit:
            return CUT_OFF
        cutoff_occurred = False
        for child in neighbors(node):
            # avoid cycles within current path
            if child in path: 
                continue
            result = recursive_dls(child, path + [child], depth + 1)
            if result is CUT_OFF:
                cutoff_occurred = True
            elif result is not FAILURE:
                return result
        return CUT_OFF if cutoff_occurred else FAILURE

    return recursive_dls(start, [start], 0)

# example: grid/graph search
start = 'A'
goal = 'G'
def goal_test(s): return s == goal
graph = {
  'A': ['B','C'],
  'B': ['D','E'],
  'C': ['F'],
  'D': [], 'E': ['G'], 'F': [], 'G': []
}
def neighbors(s): return graph.get(s, [])

path = depth_limited_search(start, goal_test, neighbors, limit=2)
print(path)
# -> returns CUT_OFF here (because G is at depth 3), try limit=3

def iterative_deepening_search(start, goal_test, neighbors, max_limit=50):
    for L in range(max_limit + 1):
        result = depth_limited_search(start, goal_test, neighbors, L)
        if result is not CUT_OFF and result is not FAILURE:
            return result
    return FAILURE

from collections import deque

def _reconstruct(meet, parent_s, parent_t):
    # build start -> meet
    left = []
    x = meet
    while x is not None:
        left.append(x)
        x = parent_s.get(x)
    left.reverse()
    # build meet -> goal using parents from goal side (they point toward goal)
    right = []
    x = parent_t.get(meet)  # skip meet duplication
    while x is not None:
        right.append(x)
        x = parent_t.get(x)
    return left + right

def bidirectional_bfs(start, goal, neighbors, reverse_neighbors=None):
    """
    Shortest path (by hops) using BFS from both start and goal.
    neighbors(s): iterable of forward neighbors
    reverse_neighbors(s): iterable of predecessors (for directed graphs).
                          If None, uses neighbors (OK for undirected graphs).
    Returns: list of states from start to goal, or None if no path.
    """
    if start == goal:
        return [start]
    if reverse_neighbors is None:
        reverse_neighbors = neighbors  # undirected case

    # frontier queues
    q_s = deque([start])
    q_t = deque([goal])

    # visited + parents for path reconstruction
    visited_s = {start}
    visited_t = {goal}
    parent_s = {start: None}
    parent_t = {goal: None}

    # alternate expansions (you can also expand the smaller frontier each step)
    while q_s and q_t:
        # expand from start side
        for _ in range(len(q_s)):  # one BFS layer
            u = q_s.popleft()
            for v in neighbors(u):
                if v not in visited_s:
                    visited_s.add(v)
                    parent_s[v] = u
                    if v in visited_t:              # meeting point found
                        return _reconstruct(v, parent_s, parent_t)
                    q_s.append(v)

        # expand from goal side
        for _ in range(len(q_t)):  # one BFS layer (backwards graph)
            u = q_t.popleft()
            for v in reverse_neighbors(u):
                if v not in visited_t:
                    visited_t.add(v)
                    parent_t[v] = u
                    if v in visited_s:              # meeting point found
                        return _reconstruct(v, parent_s, parent_t)
                    q_t.append(v)

    return None

graph = {
    'A': ['B','C'],
    'B': ['A','D','E'],
    'C': ['A','F'],
    'D': ['B'],
    'E': ['B','G'],
    'F': ['C'],
    'G': ['E']
}
def neighbors(u): return graph.get(u, [])

path = bidirectional_bfs('A', 'G', neighbors)
# -> ['A','B','E','G']
print(path)