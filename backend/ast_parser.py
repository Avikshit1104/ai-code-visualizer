import ast
import json

def parse_code(code):
    tree = ast.parse(code)

    def node_to_dict(node):
        result = {"type": type(node).__name__}

        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                result[field] = node_to_dict(value)
            elif isinstance(value, list):
                result[field] = [
                    node_to_dict(item) if isinstance(item, ast.AST) else item
                    for item in value
                ]
            else:
                result[field] = value

        return result

    return node_to_dict(tree)


if __name__ == "__main__":
    code = """
for i in range(5):
    print(i)
"""

    ast_tree = parse_code(code)
    print(json.dumps(ast_tree, indent=2))