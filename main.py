# 1 Evaluate into RPN
# 1.1 extract each digit and operator and enter into an array in the same order given
def checkpos(val):
    if val == " ":
        return True
    else:
        return False


# TODO clean up
#   RPN conversion

def arrayconversion(equation):  # WORKS
    data = []
    value = ""
    operator = True
    for pos in equation:
        if pos == " ":
            continue
        elif not operator and (pos == "*" or pos == "/" or pos == "+" or pos == "^"):
            if len(value) > 0: data.append(float(value)); value = ""
            data.append(pos); operator = True
        elif pos == "(" or pos == ")":
            if len(value) > 0: data.append(float(value)); value = ""
            data.append(pos)
            if pos == "(": operator = True
        elif pos == "-":  # for negatives
            if value == "-": value = ""  # precaution for double negatives
            elif not operator:
                if len(value) > 0:
                    data.append(float(value)); value = ""
                else: data.append(pos); operator = True
            # adds the value to the array followed by a negative if there is not an operator before
            else: value += pos  # adds the negative to the value
        elif pos.isdigit() or pos == ".": value += pos; operator = False  # adds the digit to the value
    if len(value) > 0:
        data.append(float(value))  # making sure that the last value is in the array before RPN conversion
    return data


def stackcheck(data, array):  # send array[i] and stack from rpn conversion
    # Compares the operator to the last one on the stack if the data is less important than the stack data then the
    # stack data is popped off and added to the array, else the data is added to the stack (in rpnConversion)
    importance = {"+": 1, "-": 1, "*": 2, "/": 2, "(": -1, ")": -1, "^": 3}
    length = len(array)
    if data == "(" or data == ")":
        return False
    elif length > 0:
        value = importance[array[len(array) - 1]]
        if value > importance[data]:
            return True
    return False


# 1.2 using a dictionary array saying the order of operator importance, evaluate into RPN
def rpnconversion(array):
    rpnarray = []
    stack = []
    for pos in array:
        if isinstance(pos, float): rpnarray.append(pos)  # if the value is a number append to array
        else:
            if pos == ")":  # if pos is a close bracket
                value = stack.pop()  # pop the first value off the stack
                while value != "(":  # while the value is not the open bracket
                    rpnarray.append(value)  # append the operator to the stack
                    value = stack.pop()
                value = ""
            else:  # if pos is anything else, an operator
                if len(stack) > 0:
                    while stackcheck(pos, stack): rpnarray.append(stack.pop())  # Description in stack check
                stack.append(pos)
    if len(stack) > 1: stack.reverse()
    for op in stack: rpnarray.append(op)

    return rpnarray


# 2 Solve the equation
def addition(b, a): return a + b
def subtraction(b, a): return a - b
def multiplication(b, a): return a * b
def division(b, a): return a / b
def power(b, a): return a ** b


# 2.1 Traverse the array L to R
def evaluate(array):
    evaluationstack = []
    for i in range(len(array)):  # loops through the array adding digits to stack/popping them off when operator
        # encountered
        if isinstance(array[i], float): evaluationstack.append(array[i])  # adding digit to stack
        else:  # operator evaluation, adds the number back onto stack once finished
            if array[i] == "+": evaluationstack.append(addition(evaluationstack.pop(), evaluationstack.pop()))
            elif array[i] == "-": evaluationstack.append(subtraction(evaluationstack.pop(), evaluationstack.pop()))
            elif array[i] == "*": evaluationstack.append(multiplication(evaluationstack.pop(), evaluationstack.pop()))
            elif array[i] == "/": evaluationstack.append(division(evaluationstack.pop(), evaluationstack.pop()))
            elif array[i] == "^": evaluationstack.append(power(evaluationstack.pop(), evaluationstack.pop()))
    print(evaluationstack.pop())


# 2.2 Using a stack to store values before an operator is found
# 2.3 Once operator is found the pop the first two items off the stack and evaluate
# 2.3 Add the evaluated value back onto the stack

equationInput = input("Please input the equation for evaluation: ")
evaluate(rpnconversion(arrayconversion(equationInput)))

