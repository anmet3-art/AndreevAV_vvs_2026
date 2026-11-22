first = float(input("Первое число: "))
operation = input("Операция (+, -, *, /): ").strip()
second = float(input("Второе число: "))
if operation == "+": result = first + second
elif operation == "-": result = first - second
elif operation == "*": result = first * second
elif operation == "/" and second != 0: result = first / second
else: result = None
print("Результат:", result if result is not None else "операция невозможна")
