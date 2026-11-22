from pathlib import Path
import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 180)
DATA = Path(__file__).with_name("titanic.csv")

def main():
    frame = pd.read_csv(DATA)
    print("Загружен набор:", DATA.name)
    amount = int(input("Сколько первых строк показать? "))
    print("\nПервые строки:\n", frame.head(amount))
    print("\nПоследние пять:\n", frame.tail())
    print("\nРазмер:", frame.shape)
    print("\nПоля:", frame.columns.tolist())
    print("\nТипы:\n", frame.dtypes)
    numeric = ["PassengerId","Age","SibSp","Parch","Fare"]
    categorical = ["Survived","Pclass","Name","Sex","Ticket","Cabin","Embarked"]
    print("\nЧисловые признаки:", numeric)
    print("Категориальные признаки:", categorical)
    summary = frame[numeric].describe().T
    summary["median"] = frame[numeric].median()
    print("\nОписательная статистика:\n", summary[["mean","median","min","max","std"]])
    print("\nРаспределение классов:\n", frame["Pclass"].value_counts().sort_index())
    print("\nУникальных портов:", frame["Embarked"].nunique())
    original_shape = frame.shape

    missing = frame.isna().sum()
    print("\nПропуски по полям:\n", missing)
    print("\nДоля пропусков, %:\n", (frame.isna().mean()*100).round(2))
    print("\nБольше всего пропусков:", missing.idxmax())
    age_stats_before = frame["Age"].agg(["mean","median","min","max","std","count"])
    print("\nВозраст до заполнения:\n", age_stats_before)
    age_median = frame["Age"].median()
    frame["Age"] = frame["Age"].fillna(age_median)
    age_stats_after = frame["Age"].agg(["mean","median","min","max","std","count"])
    print("\nВозраст после заполнения медианой:\n", age_stats_after)
    print("\nСравнение возраста:\n", pd.concat(
        [age_stats_before.rename("До"), age_stats_after.rename("После")], axis=1))
    frame = frame.dropna(subset=["Embarked"])
    cabin_ratio = frame["Cabin"].isna().mean()
    print(f"\nПропуски Cabin: {cabin_ratio:.1%}")
    if cabin_ratio > .5:
        frame = frame.drop(columns="Cabin")
        print("Cabin удалён: пропусков больше половины")
    print("\nОставшиеся пропуски:\n", frame.isna().sum())
    print("Размер до очистки:", original_shape, "| после:", frame.shape)

    values = frame["Survived"].to_numpy()
    sexes = frame["Sex"].to_numpy()
    ages = frame["Age"].to_numpy()
    print("\nДоля выживших, %:", round(values.mean()*100,2))
    for sex in ("male","female"):
        mask = sexes == sex
        print(f"Выживаемость {sex}, %:", round(values[mask].mean()*100,2))
        print(f"Средний возраст {sex}:", round(ages[mask].mean(),2))
        for outcome, label in ((1,"выжившие"),(0,"погибшие")):
            subset = ages[mask & (values==outcome)]
            print(f"Возраст: {sex}, {label}:", round(subset.mean(),2) if len(subset) else "нет наблюдений")
    print("\nЦена билета min/max/mean:",
          round(frame.Fare.min(),2), round(frame.Fare.max(),2), round(frame.Fare.mean(),2))
    print("Стандартное отклонение возраста:", round(ages.std(),2))

    filters = {
        "Мужчины старше 30 лет из первого класса":
            (frame.Sex=="male") & (frame.Age>30) & (frame.Pclass==1),
        "Выжившие женщины или дети":
            ((frame.Age<18) | (frame.Sex=="female")) & (frame.Survived==1),
        "Третий класс: билет дороже среднего для класса":
            (frame.Pclass==3) & (frame.Fare>frame.loc[frame.Pclass==3,"Fare"].mean()),
        "Пассажиры 20–40 лет, порт S":
            frame.Age.between(20,40) & (frame.Embarked=="S"),
    }
    for title, mask in filters.items():
        result=frame.loc[mask]
        print(f"\nФильтр: {title}\nКоличество: {len(result)}")
        print(result.head(10))

    by_class_sex = frame.groupby(["Pclass","Sex"]).agg(
        passengers=("PassengerId","count"), average_age=("Age","mean"),
        survival_percent=("Survived",lambda col: round(col.mean()*100,2)),
        average_fare=("Fare","mean"))
    by_port = frame.groupby("Embarked").agg(
        passengers=("PassengerId","count"),
        survival_percent=("Survived",lambda col: round(col.mean()*100,2)))
    by_class = frame.groupby("Pclass")["Survived"].mean()
    print("\nКласс и пол:\n",by_class_sex)
    print("\nПорт отправления:\n",by_port)
    print("\nДоля выживших по классам:\n",by_class)
    print("Лидирующий класс:",by_class.idxmax())
    frame.to_csv(DATA.with_name("titanic_cleaned.csv"),index=False)
    by_class_sex.to_csv(DATA.with_name("class_gender_report.csv"))
    print("\nСохранены titanic_cleaned.csv и class_gender_report.csv")
    restored=pd.read_csv(DATA.with_name("titanic_cleaned.csv"))
    print("Повторное чтение:",restored.shape,"; размер совпадает:",restored.shape==frame.shape)

if __name__=="__main__": main()
