import os
import trimesh
from pathlib import Path
from src.adaptive_isotropic_remeshing import adaptive_isotropic_remeshing

file_path = "bunny/reconstruction/bun_zipper_res2.ply"
mesh = trimesh.load(file_path)

new_folder = "reconstruction_" + "bun_zipper_res2.ply"
new_folder_path = Path(new_folder)
os.mkdir(new_folder_path)
os.chdir(new_folder_path)
epsilon = 0.01
remeshed_mesh = trimesh.Trimesh(mesh.vertices, mesh.faces)
remeshed_mesh = adaptive_isotropic_remeshing(remeshed_mesh, epsilon)
print(f"Remeshed mesh - Vertices: {len(remeshed_mesh.vertices)}, Faces: {len(remeshed_mesh.faces)}")