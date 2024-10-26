import sys
import trimesh
import numpy as np
from src.sizing_field import sizing_field

def collapse_edges(mesh, epsilon): 
    new_faces = mesh.faces.tolist() 
    vertices_to_remove = []
    collapsed_vertices = set()

    for edge_idx, edge in enumerate(mesh.edges): 
        percentage_done = (edge_idx + 1) / len(mesh.edges) * 100
        sys.stdout.write(f"\rcollapse edges: {percentage_done:.2f}%")
        sys.stdout.flush()

        v0, v1 = edge
        edge_length = np.linalg.norm(mesh.vertices[v0] - mesh.vertices[v1])
        sizing_value_vertex = sizing_field(mesh, [mesh.vertices[v0], mesh.vertices[v1]], epsilon)
        target_length = (sizing_value_vertex[0] + sizing_value_vertex[1]) / 2

        if edge_length < 4.0 / 5.0 * target_length:
            if v0 in collapsed_vertices or v1 in collapsed_vertices:
                continue
        
            midpoint = (mesh.vertices[v0] + mesh.vertices[v1]) / 2
            mesh.vertices[v0] = midpoint
            vertices_to_remove.append(v1)
            collapsed_vertices.add(v0)
            collapsed_vertices.add(v1)

            adjacent_faces = [face for face in new_faces if v0 not in face and v1 in face]

            for face in adjacent_faces: 
                new_faces.remove(face)
                v2, v3 = [v for v in face if v != v1]
                new_faces.append([v0, v2, v3])
                collapsed_vertices.add(v2)
                collapsed_vertices.add(v3)

    index_map = {}
    new_index = 0
    for old_index in range(len(mesh.vertices)):
        if old_index not in vertices_to_remove:
            index_map[old_index] = new_index
            new_index += 1
    
    if vertices_to_remove:
        new_vertices = np.delete(mesh.vertices, vertices_to_remove, axis=0)
    else:
        new_vertices = mesh.vertices.copy()

    new_faces = [
        [index_map[v] for v in face if v in index_map]
        for face in new_faces
        if all(v in index_map for v in face)  # Ensure all vertices in the face are valid
    ]
    
    mesh = trimesh.Trimesh(vertices=new_vertices, faces=new_faces)
    return mesh