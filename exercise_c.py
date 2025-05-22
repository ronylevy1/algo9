import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.layout import bipartite_layout

# Seed for reproducibility (remove for full randomness)
random.seed(42)

# --- Create a balanced bipartite graph K4,4 ---
left_nodes = random.sample(["Ami", "Tami", "Rami", "Sami", "Yami", "Nami", "Lami"], 4)
right_nodes = random.sample(["A", "B", "C", "D", "E", "F"], 4)

# Assign probabilities on edges so that for each right node the weights sum to 1
edge_weights = {}
for r in right_nodes:
    raw = [random.random() for _ in left_nodes]
    total = sum(raw)
    for l, x in zip(left_nodes, raw):
        edge_weights[(l, r)] = x / total

# Build initial weighted graph
G0 = nx.Graph()
G0.add_nodes_from(left_nodes, bipartite=0)
G0.add_nodes_from(right_nodes, bipartite=1)
for (l, r), w in edge_weights.items():
    G0.add_edge(l, r, weight=w)

# Greedy matching sequence: pick edges in random order, match if both ends free,
# then remove all incident edges, recording each intermediate graph.
def greedy_sequence(G, left_nodes, right_nodes):
    G_curr = G.copy()
    sequence = [G_curr.copy()]
    free_left = set(left_nodes)
    free_right = set(right_nodes)
    edges = list(G_curr.edges(data="weight"))
    random.shuffle(edges)
    matching = []
    for u, v, w in edges:
        if u in free_left and v in free_right:
            matching.append((u, v, w))
            # remove all edges incident to u or v
            to_remove = list(G_curr.edges(u)) + list(G_curr.edges(v))
            G_curr.remove_edges_from(to_remove)
            sequence.append(G_curr.copy())
            free_left.remove(u)
            free_right.remove(v)
    return matching, sequence

# Run 1
matching1, seq1 = greedy_sequence(G0, left_nodes, right_nodes)
# Run 2 (ensure different matching)
while True:
    matching2, seq2 = greedy_sequence(G0, left_nodes, right_nodes)
    set1 = {(u, v) for u, v, _ in matching1}
    set2 = {(u, v) for u, v, _ in matching2}
    if set1 != set2:
        break

# Print matchings
print("=== Matching 1 ===")
for u, v, w in matching1:
    print(f"{u} ↔ {v} (p={w:.2f})")

print("\n=== Matching 2 ===")
for u, v, w in matching2:
    print(f"{u} ↔ {v} (p={w:.2f})")

# Function to draw a sequence of graphs
def draw_sequence(seq, title):
    for i, G in enumerate(seq):
        plt.figure(figsize=(5, 4))
        pos = bipartite_layout(G, left_nodes)
        # collect and format weights
        labels = { (u,v): f"{w:.2f}" for u,v,w in G.edges(data="weight") }
        nx.draw(G, pos, with_labels=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title(f"{title} – Stage {i}")
        plt.axis('off')

# Draw sequences
draw_sequence(seq1, "Run 1")
draw_sequence(seq2, "Run 2")

plt.show()
