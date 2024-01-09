def greedy_coloring(graph):
    nodes = sorted(graph.nodes(), key=lambda x: -graph.degree(x))
    colors = {}
    for node in nodes:
        neighbor_colors = {colors[neighbor] for neighbor in graph.neighbors(node) if neighbor in colors}
        color = 0
        while color in neighbor_colors:
            color += 1
        colors[node] = color
    return colors



def welsh_powell_coloring(graph):
    degrees = [(vertex, len(neighbors)) for vertex, neighbors in graph.adjacency()]
    sorted_degrees = sorted(degrees, key=lambda x: x[1], reverse=True)

    colors = {}
    vertices = [vertex for vertex, _ in sorted_degrees]

    for vertex in vertices:
        # Récupérer les couleurs des voisins
        neighbor_colors = {colors[n] for n in graph.neighbors(vertex) if n in colors}
        
        # Trouver la première couleur disponible
        for color in range(len(vertices)):
            if color not in neighbor_colors:
                colors[vertex] = color
                break

    chromatic_number = max(colors.values()) + 1 if colors else 0

    return colors, chromatic_number


def welsh_powell_coloring_dynamic(graph):
    def welsh_powell_coloring_internal(graph):
        nodes = sorted(graph.nodes(), key=lambda node: -len(list(graph.neighbors(node))))
        colors = {}
        for node in nodes:
            used_colors = {colors[n] for n in graph.neighbors(node) if n in colors}
            for color in range(len(graph.nodes())):
                if color not in used_colors:
                    colors[node] = color
                    break
        return colors

    coloring = welsh_powell_coloring_internal(graph)

    def update_coloring(event):
        nonlocal coloring
        if event['action'] == 'add_node':
            graph.add_node(event['node'])
        elif event['action'] == 'remove_node':
            graph.remove_node(event['node'])
        elif event['action'] == 'add_edge':
            graph.add_edge(event['node1'], event['node2'])
        elif event['action'] == 'remove_edge':
            graph.remove_edge(event['node1'], event['node2'])
        coloring = welsh_powell_coloring_internal(graph)
        return coloring

    return coloring, update_coloring


def backtrack_coloring(graph):
    def is_safe(node, color, colors):
        return all(colors.get(neighbor) != color for neighbor in graph.neighbors(node))

    def backtrack(nodes, colors):
        if not nodes:
            return True, colors

        node = nodes[0]
        for color in range(max_colors):
            if is_safe(node, color, colors):
                colors[node] = color
                success, result = backtrack(nodes[1:], colors)
                if success:
                    return True, result
                # Undo the current color assignment
                colors[node] = None
        return False, None

    nodes = list(graph.nodes())
    max_colors = len(nodes)
    colors = {node: None for node in nodes}
    
    success, result = backtrack(nodes, colors)
    if success:
        return result
    else:
        raise ValueError("No valid coloring found.")