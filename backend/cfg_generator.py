import ast
import networkx as nx
import matplotlib.pyplot as plt

class CFGBuilder(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.prev_node = None
        self.node_count = 0

    def add_node(self, label):
        node_id = f"node_{self.node_count}"
        self.graph.add_node(node_id, label=label)

        if self.prev_node:
            self.graph.add_edge(self.prev_node, node_id)

        self.prev_node = node_id
        self.node_count += 1

    def visit_For(self, node):
        self.add_node("For Loop")

        self.visit(node.iter)

        for stmt in node.body:
            self.visit(stmt)

        self.add_node("Loop Back")

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.add_node(f"Call {node.func.id}")

    def visit_Expr(self, node):
        self.visit(node.value)


def visualize_cfg(code):

    tree = ast.parse(code)

    builder = CFGBuilder()
    builder.visit(tree)

    G = builder.graph

    pos = nx.spring_layout(G)

    labels = {node:data["label"] for node,data in G.nodes(data=True)}

    nx.draw(G,pos,labels=labels,with_labels=True,node_size=2500)

    plt.show()


if __name__ == "__main__":

    code = """
for i in range(5):
    print(i)
"""

    visualize_cfg(code)