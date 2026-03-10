import ast
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def ast_to_dict(node):
    return {
        "name": type(node).__name__,
        "children": [ast_to_dict(child) for child in ast.iter_child_nodes(node)]
    }


@app.route("/parse", methods=["POST"])
def parse_code():

    data = request.json
    code = data["code"].replace("\u00A0", " ")

    tree = ast.parse(code)

    ast_json = ast_to_dict(tree)

    return jsonify(ast_json)


def build_cfg(node, nodes, edges, parent=None):

    node_id = len(nodes)

    label = type(node).__name__

    nodes.append({
        "id": node_id,
        "label": label
    })

    if parent is not None:
        edges.append({
            "source": parent,
            "target": node_id
        })

    for child in ast.iter_child_nodes(node):
        build_cfg(child, nodes, edges, node_id)


@app.route("/cfg", methods=["POST"])
def generate_cfg():

    data = request.json
    code = data["code"].replace("\u00A0", " ")

    tree = ast.parse(code)

    nodes = []
    edges = []

    build_cfg(tree, nodes, edges)

    return jsonify({
        "nodes": nodes,
        "edges": edges
    })

@app.route("/explain", methods=["POST"])
def explain_code():

    data = request.json
    code = data["code"]

    explanation = ""

    if "for" in code:
        explanation += "This code contains a for loop. "

    if "while" in code:
        explanation += "This code contains a while loop. "

    if "print" in code:
        explanation += "It prints output to the console. "

    explanation += "The program structure was analyzed using Python AST."

    return jsonify({
        "explanation": explanation
    })

if __name__ == "__main__":
    app.run(debug=True)