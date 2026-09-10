# from fastapi import FastAPI
# from .api.v1.router import router as v1_router
# from .core.database import engine, Base

# app = FastAPI(title="My Tg Bot", version="1.0.0")

# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# app.include_router(v1_router, prefix="/api/v1")

from datetime import datetime

class Food:
    def __init__(self, name, cals=0, prot=0, fat=0, carbs=0):
        self.name=name
        self.cals=cals
        self.prot=prot
        self.fat=fat
        self.carbs=carbs
    def __str__(self):
        return f"{self.name}: {self.cals} ккал, {self.prot} Б, {self.fat} Ж, {self.carbs} У (на 100г)"

class User:
    def __init__(self, username, age, height, weight, goal):
        self.username=username
        self.age=age
        self.height=height
        self.weight=weight
        self.goal=goal
    def update_weight(self, new_weight):
        self.weight=new_weight
    def bern_cals_from_steps(self, steps):
        return steps *self.weight*0.0005
    def __str__(self):
        return f"Имя {self.username}, возраст {self.age}, рост {self.height}, вес {self.weight}, цель {self.goal}"

class SleepSession:
    def __init__(self, started_at: datetime, ended_at: datetime, quality):
        self.started_at=started_at
        self.ended_at=ended_at
        self.quality=quality
    def duration(self):
        delta=self.ended_at-self.started_at
        return delta.total_seconds()/3600
    def __str__(self):
        return f"Сон: {self.started_at} - {self.ended_at}, качество {self.quality}, длительность {self.duration():.1f}"

class WaterLog:
    def __init__(self, amount_ml, timestamp: datetime):
        self.amount_ml=amount_ml
        self.timestamp=timestamp
    def __str__(self):
        return f"Вода: {self.amount_ml} мл в {self.timestamp.strftime('%H:%M')}"
    
class ActivityLog:
    def __init__(self, steps, calories_burned, date):
        self.steps=steps
        self.calories_burned=calories_burned
        self.date=date
    def __str__(self):
        return f"Активность: {self.steps} шагов, {self.calories_burned:.1f} ккал, дата {self.date}"

class MoodLog:
    def __init__(self, date: datetime, mood, note=None):
        self.date=date
        self.mood=mood
        self.note=note
    def __str__(self):
        result= f"Настроение: {self.mood} ({self.date})"
        if self.note:
            result+=f", заметка: {self.note}"
        return result

class MealItem:
    def __init__(self, food:Food, grams):
        self.food=food
        self.grams=grams
    def calories(self):
        return (self.food.cals/100)*self.grams
    def protein(self):
        return (self.food.prot/100)*self.grams
    def fat(self):
        return (self.food.fat/100)*self.grams
    def carbs(self):
        return (self.food.carbs/100)*self.grams
    def __str__(self):
        return f"{self.food.name}: {self.grams} ({self.calories()} ккал, {self.protein()} Б, {self.fat()} Ж, {self.carbs()} У) "
class Meal:
    def __init__(self, meal_type, date, items=None):
        self.meal_type=meal_type
        self.date=date
        self.items=items if items is not None else []
    def add_item(self, food, grams):
        self.items.append(MealItem(food, grams))
    def total_calories(self):
        return sum(item.calories() for item in self.items)
    def total_protein(self):
        return sum(item.protein() for item in self.items)
    def total_fat(self):
        return sum(item.fat() for item in self.items)
    def total_carbs(self):
        return sum(item.carbs() for item in self.items)    
    def __str__(self):
        result=f"Прием пищи: {self.meal_type}, дата {self.date}\n"
        for item in self.items:
            result+=f" {item}\n"
        result+=(f"Итого: {self.total_calories():.1f} ккал, "
                 f"{self.total_protein():.1f} б, "
                 f"{self.total_fat():.1f} ж, "
                 f"{self.total_carbs():.1f} у")
        return result

class HealthDiary: #агрегатор
    def __init__(self, user: User):
        self.user = user
        self.meals = []
        self.sleep_sessions = []
        self.water_logs = []
        self.activity_logs = []
        self.mood_logs = []
    def add_meal(self, meal):
        self.meals.append(meal)
    def add_sleep(self, sleep):
        self.sleep_sessions.append(sleep)
    def add_water(self, water):
        self.water_logs.append(water)
    def add_activity(self, activity):
        self.activity_logs.append(activity)
    def add_mood(self, mood):
        self.mood_logs.append(mood)
        
    def total_calories(self):
        return sum(meal.total_calories() for meal in self.meals)
    def total_water_ml(self):
        return sum(w.amount_ml for w in self.water_logs)
    def average_sleep_duration(self):
        if not self.sleep_sessions:
            return 0
        total= sum(s.duration() for s in self.sleep_sessions)
        return total/len(self.sleep_sessions)
    def total_steps(self):
        return sum(a.steps for a in self.activity_logs)
    def __str__(self):
        return (f"Дневник пользователя {self.user.username}\n"
                f"Приёмов пищи: {len(self.meals)}\n"
                f"Сессий сна: {len(self.sleep_sessions)}\n"
                f"Записей воды: {len(self.water_logs)}\n"
                f"Записей активности: {len(self.activity_logs)}\n"
                f"Записей настроения: {len(self.mood_logs)}") 

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
            chose=int(input())
            if chose==0:
                break
            if chose==1:
                meal=input("Прием пищи? (завтрак, обед, ужин, перекус): ")
                date_of_meal=input("Дата? (ГГГГ-ММ-ДД): ")
                new_meal=Meal(meal, date_of_meal)
                while True:
                    add_prod=input("Добавить продукт? (Enter-нет, любой символ-да) ")
                    if add_prod:
                        foodname=input("Название продукта")
                        cals=float(input("Введите калл на 100г"))
                        prots=float(input("Введите белки на 100г"))
                        fats=float(input("Введите жиры на 100г"))
                        carbs=float(input("Введите углеводы на 100г"))
                    else:                        
                        break
                    new_food=Food(foodname, cals, prots, fats, carbs)
                    grams=float(input("Сколько грамм?: "))
                    new_meal.add_item(new_food, grams)
                diary.add_meal(new_meal)
                print(f"Добавлено: {new_meal}")
            if chose==2:
                try:
                    sleep_start=datetime.strptime(input("Начало сна (ГГГГ-ММ-ДД ЧЧ:ММ): "), "%Y-%m-%d %H:%M") 
                    sleep_end=datetime.strptime(input("конец сна (ГГГГ-ММ-ДД ЧЧ:ММ): "), "%Y-%m-%d %H:%M")
                    quality_of_sleep=int(input("Качество сна 0-10? "))
                    if sleep_end<=sleep_start:
                        print("Конец сна должен быть позже начала!")
                        continue
                except ValueError:
                    print("Неверный формат! пример: 2026-09-09 23:00")
                    continue
                new_sleep=SleepSession(sleep_start, sleep_end, quality_of_sleep)
                diary.add_sleep(new_sleep)
                print(f"Добавлено: {new_sleep}")
            if chose==3:
                amount=int(input("Сколько воды? "))
                water=WaterLog(amount, datetime.now())
                diary.add_water(water)
                print(f"Добавлено: {water}")
            if chose==4:
                steps=int(input("Сколько шагов? "))
                date=input("Дата (ГГГГ-ММ-ДД): ")
                cals=diary.user.bern_cals_from_steps(steps)
                activity=ActivityLog(steps, cals, date)
                diary.add_activity(activity)
                print(f"Добавлено: {activity}")
            if chose==5:
                mood_value=int(input("Ваше настроение от 0-10: "))
                date=input("Дата (ГГГГ-ММ-ДД): ")
                note=input("Описание? (по желанию): ")
                new_mood=MoodLog(date, mood_value, note)
                diary.add_mood(new_mood)
                print(f"Добавлено: {new_mood}")
            if chose==6:
                print(diary)
                print(f"Всего калорий: {diary.total_calories():.1f}")
                print(f"Всего воды: {diary.total_water_ml()} мл")
                print(f"Средняя длительность сна: {diary.average_sleep_duration():.1f} ч")
                print(f"Всего шагов: {diary.total_steps()}")
        except ValueError:
            print("Выберите число!")

def main():
    print("Добро пожаловать в HealthyBot (консольная версия)!")
    username=input("Ur name?: ")
    age=int(input("Age?: "))
    height=float(input("Haight?(sm): "))
    weight=float(input("Weight?(kg): "))
    goal=input("Ur goal?: ")
    user=User(username, age, height, weight, goal)
    diary=HealthDiary(user)
    print()
    run_console_menu(diary)

if __name__ == "__main__":
    main()