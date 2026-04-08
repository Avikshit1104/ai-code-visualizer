import ast
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------- AST ----------
def ast_to_dict(node):
    return {
        "type": type(node).__name__,
        "description": explain_node(node),
        "children": [ast_to_dict(child) for child in ast.iter_child_nodes(node)]
    }

def explain_node(node):
    if isinstance(node, ast.Module):
        return "Start of the program"

    elif isinstance(node, ast.FunctionDef):
        return f"Function Definition → {node.name}"

    elif isinstance(node, ast.ClassDef):
        return f"Class Definition → {node.name}"

    elif isinstance(node, ast.Return):
        return "Return statement"

    elif isinstance(node, ast.For):
        return "For loop → iteration"

    elif isinstance(node, ast.While):
        return "While loop → condition-based loop"

    elif isinstance(node, ast.If):
        return "If condition → decision making"

    elif isinstance(node, ast.Assign):
        return "Assignment → variable storing value"

    elif isinstance(node, ast.BinOp):
        return "Binary operation (math/logical)"

    elif isinstance(node, ast.Compare):
        return "Comparison operation"

    elif isinstance(node, ast.Call):
        return "Function call"

    elif isinstance(node, ast.Name):
        return f"Variable → {node.id}"

    elif isinstance(node, ast.Constant):
        return f"Constant → {node.value}"

    return "Other operation"

@app.route("/parse", methods=["POST"])
def parse_code():
    try:
        code = request.json["code"].replace("\u00A0", " ")
        tree = ast.parse(code)
        return jsonify(ast_to_dict(tree))
    except Exception as e:
        return jsonify({"error": f"Syntax Error: {str(e)}"})


# ---------- CFG ----------
def get_label(node):
    if isinstance(node, ast.Module):
        return "START"

    elif isinstance(node, ast.FunctionDef):
        return f"Function: {node.name}"

    elif isinstance(node, ast.ClassDef):
        return f"Class: {node.name}"

    elif isinstance(node, ast.For):
        return "FOR Loop"

    elif isinstance(node, ast.While):
        return "WHILE Loop"

    elif isinstance(node, ast.If):
        return "IF Condition"

    elif isinstance(node, ast.Assign):
        return "Assignment"

    elif isinstance(node, ast.Return):
        return "RETURN"

    elif isinstance(node, ast.Call):
        return "Function Call"

    return type(node).__name__


def build_cfg(node, nodes, edges, parent=None):
    node_id = len(nodes)

    label = get_label(node)

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
    try:
        code = request.json["code"].replace("\u00A0", " ")
        tree = ast.parse(code)

        nodes = []
        edges = []

        build_cfg(tree, nodes, edges)

        # Add END node
        end_id = len(nodes)
        nodes.append({"id": end_id, "label": "END"})

        if len(nodes) > 1:
            edges.append({
                "source": len(nodes) - 2,
                "target": end_id
            })

        return jsonify({"nodes": nodes, "edges": edges})

    except Exception as e:
        return jsonify({"error": f"Syntax Error: {str(e)}"})


# ---------- EXPLAIN ----------
@app.route("/explain", methods=["POST"])
def explain_code():
    try:
        code = request.json["code"]
        tree = ast.parse(code)

        explanation = "🔍 Detailed Code Explanation:\n\n"

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):
                explanation += f"Function '{node.name}' is defined.\n"

            elif isinstance(node, ast.ClassDef):
                explanation += f"Class '{node.name}' is created.\n"

            elif isinstance(node, ast.For):
                explanation += "A for loop is used for iteration.\n"

            elif isinstance(node, ast.While):
                explanation += "A while loop runs based on a condition.\n"

            elif isinstance(node, ast.If):
                explanation += "An if condition controls decision making.\n"

            elif isinstance(node, ast.Assign):
                explanation += "A variable is assigned a value.\n"

            elif isinstance(node, ast.Return):
                explanation += "A value is returned from function.\n"

            elif isinstance(node, ast.Call):
                explanation += "A function is being called.\n"

        explanation += "\n📌 Summary:\n"
        explanation += "This program structure is analyzed using AST (structure) and CFG (flow of execution)."

        return jsonify({"explanation": explanation})

    except Exception as e:
        return jsonify({"error": str(e)})


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)