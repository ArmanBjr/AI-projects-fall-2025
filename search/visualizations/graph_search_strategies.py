from collections import deque
import heapq

def graph_search(
    start,
    goal_test,
    neighbors,                 # neighbors(s) -> iterable[(next_state, action, step_cost)] or iterable[next_state]
    strategy="bfs",            # "dfs" | "bfs" | "ucs" | "astar"
    heuristic=None,            # h(s) -> estimate-to-goal (only for A*)
    return_actions=False       # if True, returns (states_path, actions_path, total_cost)
):
    """
    Generic GRAPH-SEARCH (AIMA-style) with explored set.
    - start: initial state (hashable)
    - goal_test: fn(state)->bool
    - neighbors:
        EITHER returns iterable of next_state (unweighted, no actions)
        OR returns iterable of (next_state, action, step_cost)
    - strategy: "dfs", "bfs", "ucs", "astar"
    - heuristic: required for "astar"; ignored otherwise
    - return_actions: include action sequence and cost if actions/costs provided
    Returns:
      states_path  OR  (states_path, actions_path, total_cost) if return_actions=True
      None if no solution
    """

    # Normalize neighbors to always yield (child, action, step_cost)
    def norm_neighbors(s):
        for item in neighbors(s):
            if isinstance(item, tuple) and len(item) == 3:
                yield item
            else:
                # assume item is just next_state (unweighted)
                yield (item, None, 1)

    def reconstruct(state, parent, action_to):  # parent: dict[state]->state, action_to: dict[state]->action
        states = []
        actions = []
        cur = state
        while cur is not None:
            states.append(cur)
            actions.append(action_to.get(cur))
            cur = parent.get(cur)
        states.reverse()
        actions.reverse()
        if actions and actions[0] is None:
            actions = actions[1:]  # drop the first None (action to reach start)
        if return_actions:
            # compute cost if we’ve tracked g
            total_cost = g.get(states[-1], len(states) - 1) if strategy in ("ucs","astar") else len(states) - 1
            return states, actions, total_cost
        return states

    # Data shared across strategies
    explored = set()
    parent = {start: None}
    action_to = {start: None}

    if strategy in ("dfs", "bfs"):
        # Frontier is LIFO for DFS, FIFO for BFS
        frontier = deque([start])
        in_frontier = {start}
        while frontier:
            node = frontier.pop() if strategy == "dfs" else frontier.popleft()
            in_frontier.discard(node)

            if goal_test(node):
                return reconstruct(node, parent, action_to)

            explored.add(node)
            for child, act, cost in norm_neighbors(node):
                if child in explored or child in in_frontier:
                    continue
                parent[child] = node
                action_to[child] = act
                if strategy == "dfs":
                    frontier.append(child)
                else:
                    frontier.append(child)
                in_frontier.add(child)
        return None

    elif strategy in ("ucs", "astar"):
        # Frontier is a priority queue by g (UCS) or f=g+h (A*)
        if strategy == "astar" and heuristic is None:
            raise ValueError("A* requires a heuristic(state) function.")
        g = {start: 0.0}
        # entries: (priority, state)
        def f(s): return g[s] + (heuristic(s) if strategy == "astar" else 0.0)
        pq = [(f(start), start)]
        in_frontier = {start}

        while pq:
            _, node = heapq.heappop(pq)
            in_frontier.discard(node)

            if node in explored:
                continue
            if goal_test(node):
                return reconstruct(node, parent, action_to)

            explored.add(node)
            for child, act, step in norm_neighbors(node):
                tentative = g[node] + float(step)
                if child in explored and tentative >= g.get(child, float("inf")):
                    continue
                if tentative < g.get(child, float("inf")):
                    g[child] = tentative
                    parent[child] = node
                    action_to[child] = act
                    heapq.heappush(pq, (tentative if strategy=="ucs" else tentative + heuristic(child), child))
                    in_frontier.add(child)
        return None

    else:
        raise ValueError("strategy must be one of: 'dfs','bfs','ucs','astar'")

G = {
    'A': ['B','C'],
    'B': ['A','D','E'],
    'C': ['A','F'],
    'D': ['B'],
    'E': ['B','G'],
    'F': ['C'],
    'G': ['E']
}
def neigh(s): return G.get(s, [])
def goal(s): return s == 'G'

print(graph_search('A', goal, neigh, strategy='bfs'))
# -> ['A','B','E','G']

WG = {
    'S': [('A','toA',2), ('B','toB',5)],
    'A': [('C','toC',2)],
    'B': [('C','toC',1)],
    'C': [('G','toG',3)],
    'G': []
}
def neigh_w(s): return WG.get(s, [])
def goal_g(s): return s == 'G'

print(graph_search('S', goal_g, neigh_w, strategy='ucs', return_actions=True))
# -> (['S','A','C','G'], ['toA','toC','toG'], total_cost=7.0)
