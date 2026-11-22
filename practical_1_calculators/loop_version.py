def calculate(symbol, left, right):
    if symbol == "+": return left + right
    if symbol == "-": return left - right
    if symbol == "*": return left * right
    if symbol == "/":
        if right == 0: raise ZeroDivisionError("Делитель равен нулю")
        return left / right
    raise ValueError("Неизвестный оператор")

while True:
    try:
        x = float(input("Левый операнд: "))
        op = input("Операция (+ - * /), q — выход: ").strip()
        if op.lower() == "q": break
        y = float(input("Правый операнд: "))
        print("Итого:", calculate(op, x, y))
    except (ValueError, ZeroDivisionError) as exc:
        print("Не удалось вычислить:", exc)
