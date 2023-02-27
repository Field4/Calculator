import numpy as np
# 1 Evaluate into RPN
# 1.1 extract each digit and operator and enter into an array in the same order given


def lengthcheck(val, func, arr, char, op):
    if len(val) > 0:  # SIMILAR FUNCTION
        if char == "(":
            if val == "-": val += "1"
            arr.append(float(val)); val = ""
            arr.append("*")
        else: arr.append(float(val)); val = ""
    if len(func) > 0: arr.append(func); func = ""
    if not op and char == "(": arr.append("*")
    arr.append(char)
    return val, func, arr


def arrayconversion(equation):  # converts the string equation into an array 
    data = []
    value = ""
    operator = True
    function = ""
    for pos in equation:  # cycles through every character in the array
        if pos == " ":
            continue
        elif not operator and (pos == "*" or pos == "/" or pos == "+" or pos == "^" or pos == "!" or pos == "(" or pos == ")"):  # If pos is an
            # operator then do as below
            value, function, data = lengthcheck(value, function, data, pos, operator)
            if pos != ")": operator = True  # only if not close bracket then make operator True
        elif pos == "-":
            if value == "-": value = ""  # precaution for double negatives
            elif not operator:
                value, function, data = lengthcheck(value, function, data, pos, operator)
                operator = True
            # adds the value to the array followed by a negative if there is not an operator before
            else: value += pos
        elif pos == "(":  # allows for when a bracket begins the equation
            value, function, data = lengthcheck(value, function, data, pos, operator)
        elif pos.isdigit() or pos == ".":
            value += pos; operator = False
            if len(function) > 0: data.append(function); function = ""  # SIMILAR FUNCTION
        # for trig functions
        else:
            function += pos; operator = False
            if len(value) > 0: data.append(float(value)); value = ""; data.append("*")  # SIMILAR FUNCTION
            # check if value holds anything, if so then append and clear the value, add a "*" on the end to multiply values
    if len(value) > 0:
        data.append(float(value))
    return data


def stackcheck(data, array):  # send array[i] and stack from rpn conversion
    # Compares the operator to the last one on the stack if the data is less important than the stack data then the
    # stack data is popped off and added to the array, else the data is added to the stack (in rpnConversion)
    importance = {"sin": 4, "cos": 4, "tan": 4, "!": 4, "+": 1, "-": 1, "*": 2, "/": 2, "(": -1, ")": -1, "^": 3}
    length = len(array)
    if data == "(" or data == ")":
        return False
    elif length > 0:
        value = importance[array[len(array) - 1]]
        if value > importance[data]: return True
    return False


# 1.2 using a dictionary array saying the order of operator importance, evaluate into RPN
def rpnconversion(array):
    rpnarray = []
    stack = []
    for pos in array:
        if isinstance(pos, float):
            rpnarray.append(pos)  # if the value is a number append to array
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
    if len(stack) > 1: stack.reverse()  # reverses stack so the operators get added in the correct order
    for op in stack: rpnarray.append(op)
    return rpnarray


# 2 Solve the equation
def addition(b, a): return a + b


def subtraction(b, a): return a - b


def multiplication(b, a): return a * b


def division(b, a): return a / b


def power(b, a): return a ** b


def factorial(a, i):  # recursive factorial function
    if a > 0: i *= a; a -= 1; return factorial(a, i)
    else: return i


def sine(a): return round(np.sin(np.radians(a)), 10)


def tangent(a): return round(np.tan(np.radians(a)), 10)


def cosine(a): return round(np.cos(np.radians(a)), 10)


# 2.1 Traverse the array L to R
def evaluate(array):
    evaluationstack = []
    for i in range(len(array)):  # loops through the array adding digits to stack/popping them off when operator
        # encountered
        if isinstance(array[i], float):
            evaluationstack.append(array[i])  # adding digit to stack
        else:  # operator evaluation, adds the number back onto stack once finished
            if array[i] == "+": evaluationstack.append(addition(evaluationstack.pop(), evaluationstack.pop()))
            elif array[i] == "-": evaluationstack.append(subtraction(evaluationstack.pop(), evaluationstack.pop()))
            elif array[i] == "*": evaluationstack.append(multiplication(evaluationstack.pop(), evaluationstack.pop()))
            elif array[i] == "/": evaluationstack.append(division(evaluationstack.pop(), evaluationstack.pop()))
            elif array[i] == "^": evaluationstack.append(power(evaluationstack.pop(), evaluationstack.pop()))
            elif array[i] == "!": evaluationstack.append(factorial(evaluationstack.pop(), 1))
            elif array[i] == "sin": evaluationstack.append(sine(evaluationstack.pop()))
            elif array[i] == "cos": evaluationstack.append(cosine(evaluationstack.pop()))
            elif array[i] == "tan": evaluationstack.append(tangent(evaluationstack.pop()))
    print(evaluationstack.pop())


# 2.2 Using a stack to store values before an operator is found
# 2.3 Once operator is found the pop the first two items off the stack and evaluate
# 2.3 Add the evaluated value back onto the stack

equationInput = input("Please input the equation for evaluation: ")
evaluate(rpnconversion(arrayconversion(equationInput)))
