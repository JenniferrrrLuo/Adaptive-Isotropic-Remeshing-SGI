import sys
import trimesh
import numpy as np
from src.sizing_field import sizing_field

def split_edges(mesh, epsilon): 
    new_vertices = mesh.vertices.tolist() 
    new_faces = mesh.faces.tolist() 

    for edge_idx, edge in enumerate(mesh.edges): 
        percentage_done = (edge_idx + 1) / len(mesh.edges) * 100
        sys.stdout.write(f"\rsplit edges: {percentage_done:.2f}%")
        sys.stdout.flush()

        v0, v1 = edge
        edge_length = np.linalg.norm(mesh.vertices[v0] - mesh.vertices[v1])
        sizing_value_vertex = sizing_field(mesh, [mesh.vertices[v0], mesh.vertices[v1]], epsilon)
        target_length = (sizing_value_vertex[0] + sizing_value_vertex[1]) / 2

        if edge_length > 4.0 / 3.0 * target_length:
            midpoint = (mesh.vertices[v0] + mesh.vertices[v1]) / 2
            new_vertex_index = len(new_vertices)
            new_vertices.append(midpoint)

            adjacent_faces = [face for face in new_faces if v0 in face and v1 in face]

            for face in adjacent_faces: 
                new_faces.remove(face)
                v2 = [v for v in face if v != v0 and v != v1][0]
                new_faces.append([v0, new_vertex_index, v2])
                new_faces.append([v1, new_vertex_index, v2])

    mesh = trimesh.Trimesh(vertices=new_vertices, faces=new_faces)
    return mesh