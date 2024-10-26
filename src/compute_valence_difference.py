import numpy as np

def compute_valence_difference(valence, is_boundary):
    if is_boundary: 
        ideal_valence = 4
    else: 
        ideal_valence = 6
    deviation = np.abs(valence - ideal_valence)
    return deviation