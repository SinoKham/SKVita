from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from app.models import Food

food_bd={}
next_id=1

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

def food_create_to_food(shema: FoodCreate) -> Food:
    return Food(
        name=shema.name,
        cals=shema.calories,
        prot=shema.protein,
        fat=shema.fat,
        carbs=shema.carbs
    )

def food_to_response(food_id: int, food: Food) -> FoodResponse:
    return FoodResponse(
        id=food_id,
        name=food.name,
        calories=food.cals,
        protein=food.prot,
        fat=food.fat,
        carbs=food.carbs
    )

@app.post("/foods")
def create_food(food: FoodCreate):
    global next_id
    new_food=food_create_to_food(food)
    food_bd[next_id]=new_food    
    new_id=next_id
    next_id+=1
    return food_to_response(new_id, new_food)

@app.get("/foods")
def list_foods():
    return {"foods": [food_to_response(fid, f) for fid, f in food_bd.items()]}

@app.get("/foods/{food_id}")
def get_food(food_id: int):
    if food_id in food_bd:
        food=food_bd[food_id]
        return food_to_response(food_id, food)
    else:
        raise HTTPException(status_code=404, detail="Food not found")
