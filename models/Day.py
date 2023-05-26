
from .Meal import Meal
from .MealTypes import MealType
from enum import Enum

class DayName(Enum):
    Monday = 0
    Tuseday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

class Day:
    def __init__(self,dayname: DayName) -> None:
        self.name = dayname
        self.breakfast = None
        self.lunch = None
        self.dinner = None
        self.snack = []
        self.drink = []
        self.liquor = None
        self.calcount = 0

    @property
    def caltotal(self):
        cals = 0
        if self.breakfast != None:
            cals += self.breakfast.calories
        if self.lunch != None:
            cals += self.lunch.calories
        if self.dinner != None:
            cals += self.dinner.calories
        if self.liquor != None:
            cals += self.liquor.calories
        if self.snack:
            for snack in self.snack:
                cals += snack.calories
        if self.drink:
            for drink in self.drink:
                cals += drink.calories
        return cals



        
    

