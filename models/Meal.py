from .MealTypes import MealType
import json

class Meal:
    def __init__(self, name: str, cal: int, mealtype: MealType) -> None:
        self.name = name
        self.calories = cal
        self.mealtype = mealtype
    def __str__(self) -> str:
        return self.name
    
    def to_json(self):
        return json.dumps({
            'Name': self.name,
            'Calories': self.calories,
            'Type': self.mealtype
        })
