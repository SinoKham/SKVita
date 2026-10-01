from app.database import Base
from sqlalchemy import Column, Integer, String, Float
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

class FoodModel(Base):
    __tablename__= "foods"
    id=Column(Integer, primary_key=True)
    name= Column(String)
    calories=Column(Float)
    protein=Column(Float)
    fat=Column(Float)
    carbs=Column(Float)

class UserModel(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True)
    username=Column(String)
    tg_id=Column(Integer, unique=True, nullable=False)
    created_at=Column(DateTime, default=datetime.utcnow, nullable=False)

class MealModel(Base):
    __tablename__="meals"
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    meal_type=Column(String, nullable=False)
    eat_at=Column(DateTime, default=datetime.utcnow, nullable=False)

class MealItemModel(Base):
    __tablename__="meal_items"
    id=Column(Integer, primary_key=True)
    meal_id=Column(Integer, ForeignKey("meals.id", ondelete="CASCADE"), nullable=False)
    food_id=Column(Integer, ForeignKey("foods.id"), nullable=False)
    grams=Column(Float, nullable=False)

class SleepModel(Base):
    __tablename__="sleep_sessions"
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    started_at=Column(DateTime, nullable=False)
    ended_at=Column(DateTime, nullable=False)
    quality=Column(Integer, nullable=False)

class WaterModel(Base):
    __tablename__="water_logs"
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount_ml=Column(Integer, nullable=False)
    drank_at=Column(DateTime, default=datetime.utcnow, nullable=False)

class ActivityModel(Base):
    __tablename__="activity_logs"
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date=Column(DateTime, default=datetime.utcnow, nullable=False)
    steps=Column(Integer, nullable=False)
    calories_burned=Column(Float, nullable=False)

class MoodModel(Base):
    __tablename__="mood_logs"
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date=Column(DateTime, default=datetime.utcnow, nullable=False)
    mood=Column(Integer, nullable=False)
    note=Column(String)