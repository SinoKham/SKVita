from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import FoodModel

app=FastAPI()

@app.get("/")
def read_root(): 
    return {"status": "HealthyBot API is running"}

class FoodCreate(BaseModel):
    name: str
    calories: float
    protein: float
    fat: float
    carbs: float

class FoodResponse(BaseModel):
    id: int
    name: str
    calories: float
    protein: float
    fat: float
    carbs: float

def food_create_to_food(shema: FoodCreate) -> FoodModel:
    return FoodModel(
        name=shema.name,
        calories=shema.calories,
        protein=shema.protein,
        fat=shema.fat,
        carbs=shema.carbs
    ) #тк pydantic нельзя положить в бд

def food_to_response(food: FoodModel) -> FoodResponse:
    return FoodResponse(
        id=food.id,
        name=food.name,
        calories=food.calories,
        protein=food.protein,
        fat=food.fat,
        carbs=food.carbs
    )

@app.post("/foods")
def create_food(food: FoodCreate, db: Session=Depends(get_db)):
    new_food=food_create_to_food(food)
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return food_to_response(new_food)

@app.get("/foods")
def list_foods(db: Session=Depends(get_db)):
    foods=db.query(FoodModel).all()
    return {"foods": [food_to_response(f) for f in foods]}

@app.get("/foods/{food_id}")
def get_food(food_id: int, db:Session=Depends(get_db)):
    food=db.get(FoodModel, food_id)
    if food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return food_to_response(food)
