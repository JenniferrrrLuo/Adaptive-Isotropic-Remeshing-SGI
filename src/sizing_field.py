import trimesh
import numpy as np

def sizing_field(mesh, points, epsilon):
    mean_curvature = trimesh.curvature.discrete_mean_curvature_measure(mesh, points, radius=1.0)
    gaussian_curvature = trimesh.curvature.discrete_gaussian_curvature_measure(mesh, points, radius=1.0)
    max_curvature = np.abs(mean_curvature) + np.sqrt(np.abs(mean_curvature**2 - gaussian_curvature))
    max_curvature = np.maximum(max_curvature, 1e-6)
    sizing_values = np.sqrt(np.maximum(6 * epsilon / max_curvature - 3 * epsilon**2, 0))
    return sizing_values