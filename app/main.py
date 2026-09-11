from app.models import Food, User, Meal, MealItem
from app.diary import HealthDiary
from app.console_menu import run_console_menu


def main():
    print("Добро пожаловать в HealthyBot (консольная версия)!")
    username = input("Ur name?: ")
    age = int(input("Age?: "))
    height = float(input("Haight?(sm): "))
    weight = float(input("Weight?(kg): "))
    goal = input("Ur goal?: ")
    user = User(username, age, height, weight, goal)
    diary = HealthDiary(user)
    print()
    run_console_menu(diary)


if __name__ == "__main__":
    main()
