from app.models import User


class HealthDiary:  # агрегатор
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
        total = sum(s.duration() for s in self.sleep_sessions)
        return total / len(self.sleep_sessions)

    def total_steps(self):
        return sum(a.steps for a in self.activity_logs)

    def __str__(self):
        return (
            f"Дневник пользователя {self.user.username}\n"
            f"Приёмов пищи: {len(self.meals)}\n"
            f"Сессий сна: {len(self.sleep_sessions)}\n"
            f"Записей воды: {len(self.water_logs)}\n"
            f"Записей активности: {len(self.activity_logs)}\n"
            f"Записей настроения: {len(self.mood_logs)}"
        )
