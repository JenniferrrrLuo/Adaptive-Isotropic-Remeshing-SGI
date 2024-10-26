import trimesh
import numpy as np
from src.compute_valence import compute_valence
from src.is_boundary_vertex import is_boundary_vertex
from src.compute_valence_difference import compute_valence_difference

def flip_edge_condition(vertices, edges, faces, edge):
    v1, v2 = edge
    adjacent_faces = [face for face in faces if v1 in face and v2 in face]

    if len(adjacent_faces) != 2:
        return False, None, None, None, None

    face1, face2 = adjacent_faces
    v3 = [v for v in face1 if v != v1 and v != v2]
    v4 = [v for v in face2 if v != v1 and v != v2]

    if len(v3) != 1 or len(v4) != 1 or v3[0] == v4[0]:
        return False, None, None, None, None

    v3, v4 = v3[0], v4[0]

    if any(np.array_equal([v3, v4], edge) for edge in edges):
        return False, None, None, None, None

    # Calculate the normal vectors of the two triangles
    normal1 = np.cross(vertices[face1[1]] - vertices[face1[0]], vertices[face1[2]] - vertices[face1[0]])
    normal2 = np.cross(vertices[face2[1]] - vertices[face2[0]], vertices[face2[2]] - vertices[face2[0]])

    # Normalize the normals
    normal1 /= np.linalg.norm(normal1)
    normal2 /= np.linalg.norm(normal2)

    # Check if the normals are aligned (same surface)
    dot_product = np.dot(normal1, normal2)

    if dot_product < 0.9: # do not flip sharp edges
        return False, None, None, None, None

    valence = compute_valence(vertices, edges)
    is_boundary_v1 = is_boundary_vertex(v1, edges)
    is_boundary_v2 = is_boundary_vertex(v2, edges)
    is_boundary_v3 = is_boundary_vertex(v3, edges)
    is_boundary_v4 = is_boundary_vertex(v4, edges)

    difference_before = compute_valence_difference(valence[v1], is_boundary_v1)**2 + \
                        compute_valence_difference(valence[v2], is_boundary_v2)**2 + \
                        compute_valence_difference(valence[v3], is_boundary_v3)**2 + \
                        compute_valence_difference(valence[v4], is_boundary_v4)**2

    difference_after = compute_valence_difference(valence[v1] - 1, is_boundary_v1)**2 + \
                       compute_valence_difference(valence[v2] - 1, is_boundary_v2)**2 + \
                       compute_valence_difference(valence[v3] + 1, is_boundary_v3)**2 + \
                       compute_valence_difference(valence[v4] + 1, is_boundary_v4)**2

    return difference_after < difference_before, v3, v4, face1, face2

def flip_edges(mesh, edge):
    condition, v3, v4, face1, face2 = flip_edge_condition(mesh.vertices, mesh.edges_unique, mesh.faces, edge)

    if not condition:
        return mesh

    v1, v2 = edge
    new_faces = np.array([face for face in mesh.faces if not np.array_equal(face, face1) and not np.array_equal(face, face2)])
    new_faces = np.vstack([new_faces, sorted([v1, v3, v4]), sorted([v2, v3, v4])])
    new_mesh = trimesh.Trimesh(vertices=mesh.vertices, faces=new_faces)

    return new_mesh