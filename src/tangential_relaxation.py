import trimesh
import numpy as np

def tangential_relaxation(mesh, L):
    vertices = mesh.vertices
    faces = mesh.faces
    relaxed_vertices = np.zeros_like(vertices)

    for i in range(len(vertices)):
        incident_faces = np.where(faces == i)[0]
        weighted_barycenter_sum = np.zeros(3)
        weight_sum = 0

        for face_idx in incident_faces:
            face_vertices = faces[face_idx]
            triangle_vertices = vertices[face_vertices]
            barycenter = np.mean(triangle_vertices, axis=0)

            v0, v1, v2 = triangle_vertices
            area = np.linalg.norm(np.cross(v1 - v0, v2 - v0)) / 2.0

            sizing_at_barycenter = np.mean([L[v] for v in face_vertices])
            weight = area * sizing_at_barycenter
            weighted_barycenter_sum += weight * barycenter
            weight_sum += weight

        relaxed_vertices[i] = weighted_barycenter_sum / weight_sum if weight_sum != 0 else vertices[i]

    relaxed_mesh = trimesh.Trimesh(vertices=relaxed_vertices, faces=faces)

    return relaxed_mesh