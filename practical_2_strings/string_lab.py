import re
import string

def level_case():
    sample = input("Введите фразу для преобразования: ")
    print("1 — верхний регистр, 2 — нижний, 3 — Заглавная")
    choice = input("Ваш выбор: ").strip()
    actions = {"1": str.upper, "2": str.lower, "3": str.capitalize}
    if choice in actions: print(actions[choice](sample))
    else: print("Нет такого варианта")

def level_substrings():
    source = input("Исходный текст: ")
    fragment = input("Подстрока: ")
    print("Позиция:", source.find(fragment))
    print("Количество:", source.count(fragment))
    old = input("Что заменить: ")
    new = input("На что заменить: ")
    limit = input("Количество замен (пусто — все): ")
    try: print("Новый текст:", source.replace(old, new, -1 if not limit else int(limit)))
    except ValueError: print("Количество должно быть целым")

def level_split_join():
    raw = input("Строка для разделения: ")
    separator = input("Разделитель: ")
    parts = raw.split(separator) if separator else raw.split()
    print("Элементы:", parts)
    glue = input("Разделитель для обратной сборки: ")
    print("Собранная строка:", glue.join(parts))

def level_checks():
    value = input("Введите строку: ")
    print("Только буквы:", value.isalpha())
    print("Только цифры:", value.isdigit())
    print("Есть ли пробелы:", any(ch.isspace() for ch in value))
    print("Начинается с заглавной:", value[:1].isupper())
    print("Без внешних пробелов:", repr(value.strip()))
    print("Замена пробелов на подчёркивания:", value.replace(" ", "_"))

def normalize_text(text):
    text = re.sub(r"\s+", " ", text).strip()
    # Убираем пробелы перед знаками и добавляем пробел после знака, если его нет.
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"([,.;:!?])(?=\S)", r"\1 ", text)
    if text:
        text = text[0].upper() + text[1:]
        if text[-1] not in ".!?": text += "."
    return text

def level_editor():
    print("Введите текст с лишними пробелами и ошибочными пробелами у знаков:")
    print("Результат:", normalize_text(input("> ")))

LEVELS = {
    "1": ("Регистр символов", level_case),
    "2": ("Поиск и замена фрагментов", level_substrings),
    "3": ("Разбиение и объединение", level_split_join),
    "4": ("Проверки и преобразования", level_checks),
    "5": ("Текстовый редактор", level_editor),
}
def main():
    while True:
        print("\n=== ТРЕНАЖЁР СТРОК ===")
        for key, (title, _) in LEVELS.items(): print(f"{key}. {title}")
        print("0. Завершить")
        selected = input("Уровень: ").strip()
        if selected == "0": return
        if selected not in LEVELS:
            print("Выберите уровень от 1 до 5")
            continue
        LEVELS[selected][1]()
        if input("Ещё один уровень? (д/н): ").strip().lower() in ("н", "нет"):
            return
if __name__ == "__main__": main()
