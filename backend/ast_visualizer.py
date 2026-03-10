import ast
import networkx as nx
import matplotlib.pyplot as plt

def build_graph(node, graph, parent=None):
    node_name = type(node).__name__ + "_" + str(id(node))
    graph.add_node(node_name, label=type(node).__name__)

    if parent:
        graph.add_edge(parent, node_name)

    for child in ast.iter_child_nodes(node):
        build_graph(child, graph, node_name)


def visualize_ast(code):
    tree = ast.parse(code)
    graph = nx.DiGraph()

    build_graph(tree, graph)

    pos = nx.spring_layout(graph)

    labels = {node: data["label"] for node, data in graph.nodes(data=True)}

    nx.draw(graph, pos, labels=labels, with_labels=True, node_size=2000)
    plt.show()


if __name__ == "__main__":
    code = """
for i in range(5):
    print(i)
"""

    visualize_ast(code)