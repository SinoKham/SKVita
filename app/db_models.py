from app.database import Base
from sqlalchemy import Column, Integer, String, Float

class FoodModel(Base):
    __tablename__= "foods"
    id=Column(Integer, primary_key=True)
    name= Column(String)
    calories=Column(Float)
    protein=Column(Float)
    fat=Column(Float)
    carbs=Column(Float)