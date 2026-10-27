
import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.FloorDiv: operator.floordiv,
}


def evaluate(node, variables):
    if isinstance(node, ast.Constant):
        if type(node.value) is int:
            return node.value
        raise ValueError("Only integer values are supported.")

    if isinstance(node, ast.Name):
        if node.id not in variables:
            raise ValueError(f"Undefined variable: {node.id}")
        return variables[node.id]

    if isinstance(node, ast.BinOp):
        operator_type = type(node.op)

        if operator_type not in OPERATORS:
            raise ValueError("Unsupported arithmetic operator.")

        left = evaluate(node.left, variables)
        right = evaluate(node.right, variables)

        if operator_type is ast.FloorDiv and right == 0:
            raise ValueError("Division by zero.")

        return OPERATORS[operator_type](left, right)

    raise ValueError("Unsupported expression.")


def analyze(source):
    variables = {}
    steps = []
    tree = ast.parse(source)

    for statement in tree.body:
        if not isinstance(statement, ast.Assign):
            raise ValueError("Only variable assignments are supported.")

        if len(statement.targets) != 1:
            raise ValueError("Only one variable per assignment is supported.")

        target = statement.targets[0]

        if not isinstance(target, ast.Name):
            raise ValueError("Invalid assignment target.")

        value = evaluate(statement.value, variables)
        variables[target.id] = value

        steps.append({
            "line": statement.lineno,
            "code": ast.unparse(statement),
            "variables": variables.copy()
        })

    return steps


if __name__ == "__main__":
    sample_code = """x = 10
y = z + 5"""

    try:
        results = analyze(sample_code)

        for number, step in enumerate(results, start=1):
            print(f"Step {number}")
            print(f"Line: {step['line']}")
            print(f"Code: {step['code']}")
            print(f"Variables: {step['variables']}")
            print("-" * 35)

    except (ValueError, SyntaxError, ZeroDivisionError) as error:
        print(f"Error: {error}")
