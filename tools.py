import ast
import operator


# Allowed mathematical operators
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}


def calculate_expression(expression):
    """
    Safely evaluate a mathematical expression.

    Examples:
        21*12
        454-12+22
        2+2*4
        (10+5)*3
    """

    try:
        # Remove spaces
        expression = expression.replace(" ", "")

        # Convert expression into a Python syntax tree
        tree = ast.parse(expression, mode="eval")

        return evaluate_node(tree.body)

    except ZeroDivisionError:
        return "Error: Cannot divide by zero."

    except Exception:
        return "Error: Invalid mathematical expression."


def evaluate_node(node):

    # Number
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Invalid number")


    # Binary operation
    if isinstance(node, ast.BinOp):

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Operator not allowed")

        return operation(left, right)


    # Negative numbers
    if isinstance(node, ast.UnaryOp):

        if isinstance(node.op, ast.USub):
            return -evaluate_node(node.operand)

        if isinstance(node.op, ast.UAdd):
            return evaluate_node(node.operand)

        raise ValueError("Operator not allowed")


    raise ValueError("Expression not allowed")