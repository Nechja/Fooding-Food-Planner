from .MealTypes import MealType

class Meals:
    def __init__(self) -> None:
        self.breakfast = []
        self.lunch = []
        self.dinner = []
        self.drink = []
        self.snack = []
        self.liquor = []

    @property
    def all(self):
        return self.breakfast + self.lunch + self.dinner + self.drink + self.snack + self.liquor