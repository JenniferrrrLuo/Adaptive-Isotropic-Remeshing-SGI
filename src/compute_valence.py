import numpy as np

def compute_valence(vertices, edges):
    valence = np.zeros(len(vertices), dtype=int)
    for edge in edges:
        v1, v2 = edge
        valence[v1] += 1
        valence[v2] += 1
    return valence