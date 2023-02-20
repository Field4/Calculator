# 1 Evaluate into RPN
# 1.1 extract each digit and operator and enter into an array in the same order given
def checkpos(val):
    if val == " ":
        return True
    else:
        return False


def arrayconversion(equation):
    data = []
    i = 0
    while i < len(equation):
        if i < len(equation):
            if checkpos(equation[i]): i += 1; continue
        value = ""
        while i < len(equation) and equation[i].isdigit():
            value += equation[i]
            i += 1
        if i > 0 and value != "":
            data.append(value)
        if i < len(equation):
            if checkpos(equation[i]): i += 1; continue
            data.append(equation[i])
            i += 1
    return data


def stackcheck(data, array):
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
    operator = True
    negative = ""
    for i in range(len(array)):
        if not operator:
            negative = ""
        if array[i].isdigit():
            operator = False
            rpnarray.append(negative + array[i])
        elif array[i] == ")":
            value = stack.pop()
            while value != "(":
                rpnarray.append(value)
                if len(stack) > 0:
                    value = stack.pop()
        else:
            if operator is True and array[i] == "-":
                if len(rpnarray) == 0 and len(negative) == 1:
                    negative = ""
                    operator = True
                elif len(negative) == 1:
                    rpnarray.append(array[i])
                else:
                    negative += array[i]
            elif len(stack) > 0:
                operator = True
                while stackcheck(array[i], stack):
                    value = stack.pop()
                    rpnarray.append(value)
                stack.append(array[i])
            else:
                operator = True
                stack.append(array[i])
    if len(stack) - 1 != -1:
        while len(stack) - 1 != -1:
            value = stack.pop()
            rpnarray.append(value)
    return rpnarray


# 2 Solve the equation
def addition(b, a):
    return a + b


def subtraction(b, a):
    return a - b


def multiplication(b, a):
    return a * b


def division(b, a):
    return a / b


def power(b, a):
    return a ** b


# 2.1 Traverse the array L to R
def evaluate(array):
    evaluationstack = []
    for count in range(len(array)):
        if array[count] == " ":
            array.pop(count)
    for i in range(len(array)):
        if len(array[i]) > 1 and array[i][0] == "-":
            if array[i][1:].isdigit():
                evaluationstack.append(array[i])
        elif array[i].isdigit():
            evaluationstack.append(array[i])
        else:
            if array[i] == "+":
                evaluationstack.append(addition(float(evaluationstack.pop()), float(evaluationstack.pop())))
            elif array[i] == "-":
                evaluationstack.append(subtraction(float(evaluationstack.pop()), float(evaluationstack.pop())))
            elif array[i] == "*":
                evaluationstack.append(multiplication(float(evaluationstack.pop()), float(evaluationstack.pop())))
            elif array[i] == "/":
                evaluationstack.append(division(float(evaluationstack.pop()), float(evaluationstack.pop())))
            elif array[i] == "^":
                evaluationstack.append(power(float(evaluationstack.pop()), float(evaluationstack.pop())))
    print(evaluationstack.pop())


# 2.2 Using a stack to store values before an operator is found
# 2.3 Once operator is found the pop the first two items off the stack and evaluate
# 2.3 Add the evaluated value back onto the stack

equationInput = input("Please input the equation for evaluation: ")
evaluate(rpnconversion(arrayconversion(equationInput)))
