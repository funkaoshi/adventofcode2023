import sys

Node = tuple[int, int]
AdjacentNodes = tuple[Node, Node, Node, Node]
AdjacencyGraph = dict[Node, list[Node]]


def get_abutting_nodes(node: Node) -> AdjacentNodes:
    i, j = node
    north = (i - 1, j)
    south = (i + 1, j)
    east = (i, j + 1)
    west = (i, j - 1)
    return (north, south, east, west)


def get_adjacency_list(node: Node, value: str) -> list[Node]:
    """return the list of nodes adjecent to a given node"""

    north, south, east, west = get_abutting_nodes(node)

    match (value):
        case "|":
            # vertical pipe connecting north and south.
            return [north, south]
        case "-":
            # a horizontal pipe connecting east and west.
            return [east, west]
        case "L":
            # 90-degree bend connecting north and east.
            return [north, east]
        case "J":
            # is a 90-degree bend connecting north and west.
            return [north, west]
        case "7":
            # is a 90-degree bend connecting south and west.
            return [south, west]
        case "F":
            # is a 90-degree bend connecting south and east.
            return [south, east]
        case ".":
            # ground; there is no pipe in this tile.
            return []
        case "S":
            # starting point of animal
            return []

    # we have encountered an unknown symbol in our input
    print(f"Unknown symbol {value} at {node}")
    raise Exception


def update_adjacent_to_node(node: Node, adjacency_graph: AdjacencyGraph):
    """determine nodes adjacency list to node via the nodes that abut it."""
    for location in get_abutting_nodes(node):
        try:
            if node in adjacency_graph[location]:
                adjacency_graph[node].append(location)
        except KeyError:
            pass

    # a node can only be adjacent to two other nodes
    if len(adjacency_graph[node]) > 2:
        raise Exception


def make_graph(pipemap: list[list[str]]) -> tuple[Node, AdjacencyGraph]:
    """covert our input into a graph"""

    def valid_node(node: Node) -> bool:
        i, j = node
        return i >= 0 and j >= 0 and i < len(pipemap) and j < len(pipemap[0])

    adjacency_graph: AdjacencyGraph = {}
    for i, row in enumerate(pipemap):
        for j, node in enumerate(row):
            adjacenct_nodes = [
                node for node in get_adjacency_list((i, j), node) if valid_node(node)
            ]

            adjacency_graph[(i, j)] = adjacenct_nodes

            if node == "S":
                start = (i, j)

    # backfill the adjacency list for the start node now that we know the
    # rest of the graph (the graph is undirected).
    update_adjacent_to_node(start, adjacency_graph)

    return start, adjacency_graph


def find_furthest_node(start: Node, adjacency_graph: AdjacencyGraph) -> dict[Node, int]:
    distances: dict[Node, int] = {}
    current = [start]
    distance = 1
    while True:
        adjacenct_nodes = [node for n in current for node in adjacency_graph[n]]
        next_nodes = []
        for node in adjacenct_nodes:
            if node not in distances:
                distances[node] = distance
                next_nodes.append(node)

        if not next_nodes:
            break

        current = next_nodes

        distance += 1

    return distances


def print_map(pipemap: list[list[str]]):
    for row in pipemap:
        print(row)


filename = "input.txt" if len(sys.argv) == 1 else sys.argv[1]

with open(filename) as f:
    file = f.read().splitlines()

pipemap = [list(row) for row in file]

print_map(pipemap)

start, adjacency_graph = make_graph(pipemap)
distances = find_furthest_node(start, adjacency_graph)

print(f"Longest path is {max(distances.values())}.")
