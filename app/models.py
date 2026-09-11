from datetime import datetime
CALS_PER_STEP_FORMULA=0.0005

class Food:
    def __init__(self, name, cals=0, prot=0, fat=0, carbs=0):
        self.name = name
        self.cals = cals
        self.prot = prot
        self.fat = fat
        self.carbs = carbs

    def __str__(self):
        return f"{self.name}: {self.cals:.1f} ккал, {self.prot:.1f} Б, {self.fat:.1f} Ж, {self.carbs:.1f} У (на 100г)"


class User:
    def __init__(self, username, age, height, weight, goal):
        self.username = username
        self.age = age
        self.height = height
        self.weight = weight
        self.goal = goal

    def update_weight(self, new_weight):
        self.weight = new_weight

    def burn_cals_from_steps(self, steps):
        return steps * self.weight * CALS_PER_STEP_FORMULA

    def __str__(self):
        return f"Имя {self.username}, возраст {self.age}, рост {self.height}, вес {self.weight}, цель {self.goal}"


class SleepSession:
    def __init__(self, started_at: datetime, ended_at: datetime, quality):
        self.started_at = started_at
        self.ended_at = ended_at
        self.quality = quality

    def duration(self):
        delta = self.ended_at - self.started_at
        return delta.total_seconds() / 3600

    def __str__(self):
        started=self.started_at.strftime("%Y-%m-%d %H:%M")
        ended=self.ended_at.strftime("%Y-%m-%d %H:%M")
        return f"Сон: {started} - {ended}, качество {self.quality}, длительность {self.duration():.1f} Ч"

class WaterLog:
    def __init__(self, amount_ml, timestamp: datetime):
        self.amount_ml = amount_ml
        self.timestamp = timestamp

    def __str__(self):
        return f"Вода: {self.amount_ml} мл в {self.timestamp.strftime('%H:%M')}"

class ActivityLog:
    def __init__(self, steps, calories_burned, date):
        self.steps = steps
        self.calories_burned = calories_burned
        self.date = date

    def __str__(self):
        return f"Активность: {self.steps} шагов, {self.calories_burned:.1f} ккал, дата {self.date}"


class MoodLog:
    def __init__(self, date: datetime, mood, note=None):
        self.date = date
        self.mood = mood
        self.note = note

    def __str__(self):
        result = f"Настроение: {self.mood} ({self.date})"
        if self.note:
            result += f", заметка: {self.note}"
        return result


class MealItem:
    def __init__(self, food: Food, grams):
        self.food = food
        self.grams = grams

    def calories(self):
        return (self.food.cals / 100) * self.grams

    def protein(self):
        return (self.food.prot / 100) * self.grams

    def fat(self):
        return (self.food.fat / 100) * self.grams

    def carbs(self):
        return (self.food.carbs / 100) * self.grams

    def __str__(self):
        return f"{self.food.name}: {self.grams} г ({self.calories():.1f} ккал, {self.protein():.1f} Б, {self.fat():.1f} Ж, {self.carbs():.1f} У)"


class Meal:
    def __init__(self, meal_type, date, items=None):
        self.meal_type = meal_type
        self.date = date
        self.items = items if items is not None else []

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
        result = f"Прием пищи: {self.meal_type}, дата {self.date}\n"
        for item in self.items:
            result += f" {item}\n"
        result += (
            f"Итого: {self.total_calories():.1f} ккал, "
            f"{self.total_protein():.1f} б, "
            f"{self.total_fat():.1f} ж, "
            f"{self.total_carbs():.1f} у"
        )
        return result
