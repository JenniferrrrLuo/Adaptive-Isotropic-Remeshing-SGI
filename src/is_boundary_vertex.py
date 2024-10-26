def is_boundary_vertex(vertex, edges):
    count = 0
    for edge in edges:
        if vertex in edge:
            count += 1
    return count == 1