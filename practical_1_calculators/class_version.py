class Calculator:
    def __init__(self):
        self.actions = {"+": self._add, "-": self._sub, "*": self._mul, "/": self._div}
    def _add(self, a, b): return a + b
    def _sub(self, a, b): return a - b
    def _mul(self, a, b): return a * b
    def _div(self, a, b):
        if b == 0: raise ZeroDivisionError("Деление на ноль")
        return a / b
    def evaluate(self, operator, a, b):
        if operator not in self.actions: raise ValueError("Оператор не поддерживается")
        return self.actions[operator](a, b)

if __name__ == "__main__":
    engine = Calculator()
    while True:
        command = input("Введите выражение (например 8 * 3) или exit: ").strip()
        if command.lower() == "exit": break
        try:
            a, op, b = command.split()
            print("Результат:", engine.evaluate(op, float(a), float(b)))
        except Exception as exc:
            print("Проверьте выражение:", exc)
