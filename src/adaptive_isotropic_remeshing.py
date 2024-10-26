import sys
from src.split_edges import split_edges
from src.collapse_edges import collapse_edges
from src.flip_edges import flip_edges
from src.sizing_field import sizing_field
from src.tangential_relaxation import tangential_relaxation

def adaptive_isotropic_remeshing(mesh, epsilon, iteration = 2):
    
    for i in range(iteration): 
        print(f"iteration :", i+1)
        print(f"Original mesh - Vertices: {len(mesh.vertices)}, Faces: {len(mesh.faces)}")
        # Split or collapse edges based on epsilon
        mesh = split_edges(mesh, epsilon)
        mesh.export("mesh_after_split_iter" + str(i+1) + ".obj") 
        sys.stdout.write("\n")

        mesh = collapse_edges(mesh, epsilon)
        mesh.export("mesh_after_collapse_iter" + str(i+1) + ".obj")  # Export mesh after split or collapse
        sys.stdout.write("\n")

        # Iterate through each edge and potentially flip it
        for edge_index, edge in enumerate(mesh.edges_unique):
            percentage_done = (edge_index + 1) / len(mesh.edges_unique) * 100
            sys.stdout.write(f"\rflip edges: {percentage_done:.2f}%")
            sys.stdout.flush()
            if edge[0] < len(mesh.vertices) and edge[1] < len(mesh.vertices):
                mesh = flip_edges(mesh, edge)
        mesh.export("mesh_after_flipping_iter" + str(i+1) + ".obj")  # Export mesh after edge flipping
        sys.stdout.write("\n")

        # Apply tangential relaxation to smooth the mesh
        # Recalculate sizing values based on the updated mesh
        sizing_value_vertex = sizing_field(mesh, mesh.vertices, epsilon)
        mesh = tangential_relaxation(mesh, sizing_value_vertex)
        mesh.export("final_remeshed_mesh_iter" + str(i+1) + ".obj")  # Export final remeshed mesh

    return mesh