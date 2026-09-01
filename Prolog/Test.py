import networkx as nx
import matplotlib.pyplot as plt

# define tasks
tasks = {
    "A1": {"duration": 5, "deps": []},
    "A2": {"duration": 7, "deps": []},
    "A3": {"duration": 6, "deps": ["A1"]},
    "A4": {"duration": 7, "deps": ["A1"]},
    "A5": {"duration": 5, "deps": ["A2"]},
    "A6": {"duration": 8, "deps": ["A3"]},
    "A7": {"duration": 6, "deps": ["A4"]},
    "A8": {"duration": 4, "deps": ["A5"]},
    "A9": {"duration": 5, "deps": ["A6","A7"]},
    "A10": {"duration": 7, "deps": ["A8"]},
    "A11": {"duration": 6, "deps": ["A9"]},
    "A12": {"duration": 8, "deps": ["A10"]},
    "A13": {"duration": 5, "deps": ["A11"]},
    "A14": {"duration": 4, "deps": ["A12"]},
    "A15": {"duration": 3, "deps": ["A13","A14"]},
}

G = nx.DiGraph()
for t,info in tasks.items():
    G.add_node(t)
    for d in info["deps"]:
        G.add_edge(d,t)

plt.figure(figsize=(12,8))
pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
nx.draw(G, pos, with_labels=True, arrows=True)
plt.show()
