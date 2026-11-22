def add(x, y): return x + y
def subtract(x, y): return x - y
def multiply(x, y): return x * y
def divide(x, y):
    if y == 0: raise ZeroDivisionError("На ноль делить нельзя")
    return x / y

operations = {"+": add, "-": subtract, "*": multiply, "/": divide}
a = float(input("A = "))
sign = input("Знак операции: ").strip()
b = float(input("B = "))
try:
    print("Ответ:", operations[sign](a, b))
except (KeyError, ZeroDivisionError) as error:
    print("Ошибка:", error)
