from datetime import datetime
from app.models import Food, Meal, SleepSession, WaterLog, ActivityLog, MoodLog


def run_console_menu(diary):
    while True:
        print("Что вы хотите сделать?")
        print("1 - добавить прием пищи")
        print("2 — добавить сон")
        print("3 — добавить воду")
        print("4 — добавить активность")
        print("5 — добавить настроение")
        print("6 — показать статистику")
        print("0 — выйти")
        try:
            choice = int(input())
            if choice == 0:
                break
            elif choice == 1:
                meal = input("Прием пищи? (завтрак, обед, ужин, перекус): ")
                date_of_meal = input("Дата? (ГГГГ-ММ-ДД): ")
                new_meal = Meal(meal, date_of_meal)
                while True:
                    add_prod = input("Добавить продукт? (Enter-нет, любой символ-да) ")
                    if add_prod:
                        foodname = input("Название продукта")
                        cals = float(input("Введите калл на 100г"))
                        prots = float(input("Введите белки на 100г"))
                        fats = float(input("Введите жиры на 100г"))
                        carbs = float(input("Введите углеводы на 100г"))
                    else:
                        break
                    new_food = Food(foodname, cals, prots, fats, carbs)
                    grams = float(input("Сколько грамм?: "))
                    new_meal.add_item(new_food, grams)
                if not new_meal.items:
                    print("Приём пищи пустой, не добавлен")
                else:
                    diary.add_meal(new_meal)
                    print(f"Добавлено: {new_meal}")
            elif choice == 2:
                try:
                    sleep_start = datetime.strptime(
                        input("Начало сна (ГГГГ-ММ-ДД ЧЧ:ММ): "), "%Y-%m-%d %H:%M"
                    )
                    sleep_end = datetime.strptime(
                        input("конец сна (ГГГГ-ММ-ДД ЧЧ:ММ): "), "%Y-%m-%d %H:%M"
                    )
                    quality_of_sleep = int(input("Качество сна 0-10? "))
                    if sleep_end <= sleep_start:
                        print("Конец сна должен быть позже начала!")
                        continue
                except ValueError:
                    print("Неверный формат! пример: 2026-09-09 23:00")
                    continue
                new_sleep = SleepSession(sleep_start, sleep_end, quality_of_sleep)
                diary.add_sleep(new_sleep)
                print(f"Добавлено: {new_sleep}")
            elif choice == 3:
                amount = int(input("Сколько воды? "))
                water = WaterLog(amount, datetime.now())
                diary.add_water(water)
                print(f"Добавлено: {water}")
            elif choice == 4:
                steps = int(input("Сколько шагов? "))
                date = input("Дата (ГГГГ-ММ-ДД): ")
                cals = diary.user.burn_cals_from_steps(steps)
                activity = ActivityLog(steps, cals, date)
                diary.add_activity(activity)
                print(f"Добавлено: {activity}")
            elif choice == 5:
                mood_value = int(input("Ваше настроение от 0-10: "))
                date = input("Дата (ГГГГ-ММ-ДД): ")
                note = input("Описание? (по желанию): ")
                new_mood = MoodLog(date, mood_value, note)
                diary.add_mood(new_mood)
                print(f"Добавлено: {new_mood}")
            elif choice == 6:
                print(diary)
                print(f"Всего калорий: {diary.total_calories():.1f}")
                print(f"Всего воды: {diary.total_water_ml()} мл")
                print(
                    f"Средняя длительность сна: {diary.average_sleep_duration():.1f} ч"
                )
                print(f"Всего шагов: {diary.total_steps()}")
        except ValueError:
            print("Выберите число!")
