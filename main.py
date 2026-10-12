
class Stack:
    """A simple stack using a Python list."""
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0


def precedence(op):
    if op in ("*", "/"):
        return 2
    if op in ("+", "-"):
        return 1
    return 0


def apply_operator(values, ops):
    """Take one operator and two numbers, push the result back."""
    op = ops.pop()
    b = values.pop()
    a = values.pop()
    if op == "+":
        values.push(a + b)
    elif op == "-":
        values.push(a - b)
    elif op == "*":
        values.push(a * b)
    elif op == "/":
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        values.push(a / b)


def evaluate(expression):
    """Evaluate a math expression string using two stacks."""
    values = Stack()
    ops = Stack()
    prev = None  # previous non-space character
    i = 0
    while i < len(expression):
        ch = expression[i]
        if ch == " ":
            i += 1
            continue
        if ch.isdigit() or ch == ".":
            j = i
            while j < len(expression) and (expression[j].isdigit() or expression[j] == "."):
                j += 1
            values.push(float(expression[i:j]))
            prev = "0"
            i = j
            continue
        if ch == "(":
            ops.push(ch)
        elif ch == ")":
            while not ops.is_empty() and ops.peek() != "(":
                apply_operator(values, ops)
            if ops.is_empty():
                raise ValueError("Mismatched parentheses")
            ops.pop()  # remove "("
        elif ch in "+-*/":
            # Negative number such as -5 or (-5): treat as 0 - 5
            if ch == "-" and (prev is None or prev in "(+-*/"):
                values.push(0.0)
            while (not ops.is_empty() and ops.peek() != "("
                   and precedence(ops.peek()) >= precedence(ch)):
                apply_operator(values, ops)
            ops.push(ch)
        else:
            raise ValueError("Invalid character: " + ch)
        prev = ch
        i += 1
    while not ops.is_empty():
        if ops.peek() == "(":
            raise ValueError("Mismatched parentheses")
        apply_operator(values, ops)
    return values.pop()


def format_result(result):
    if result == int(result):
        return str(int(result))
    return str(round(result, 4))


def is_separator(line):
    s = line.strip()
    return len(s) >= 3 and set(s) == {"-"}


def read_and_evaluate(input_path):
    """Read input file, evaluate each expression, return output lines."""
    results = []
    with open(input_path, "r") as f:
        for line in f:
            text = line.strip()
            if text == "":
                continue
            if is_separator(text):
                results.append(text)  # keep the same separator
            else:
                try:
                    results.append(format_result(evaluate(text)))
                except Exception as e:
                    results.append("Error: " + str(e))
    return results


def write_output(output_path, results):
    with open(output_path, "w") as f:
        f.write("\n".join(results) + "\n")


def main():
    results = read_and_evaluate("input.txt")
    write_output("output.txt", results)
    print("Done. Results written to output.txt")


if __name__ == "__main__":
    main()