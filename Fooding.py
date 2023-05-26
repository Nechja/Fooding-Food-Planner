from models.Meal import Meal
from models.MealTypes import MealType
from models.Meals import Meals
from models.Day import Day, DayName
from tools.MealLoader import MealLoader
import pandas as pd
import json
import random

mealjsonfile = 'meals/meals.json'
cal = 0

def main():
    with open('config.json','r') as file:
        config = json.load(file)
    cal = int(config['cal'])
    meals = load_meals_from_json()
    meal_plan(meals)


def load_meals_from_json():
    meals = Meals()

    jsonmeals = MealLoader(mealjsonfile)

    for data in jsonmeals:
        meal = Meal(data['Name'],data['Calories'],MealType[data['Type']])
        if meal.mealtype == MealType.Breakfast:
            meals.breakfast.append(meal)
        elif meal.mealtype == MealType.Lunch:
            meals.lunch.append(meal)
        elif meal.mealtype == MealType.Dinner:
            meals.dinner.append(meal)
        elif meal.mealtype == MealType.Snack:
            meals.snack.append(meal)
        elif meal.mealtype == MealType.Drink:
            meals.drink.append(meal)
        elif meal.mealtype == MealType.Liquor:
            meals.liquor.append(meal)
    return meals

def meal_plan(meals: Meals):

    ##Rules
    #Lunchs, Breakfasts, Drinks, and Snacks can be repeated, but dinner can not
    #Liquor is Good on Wednesdays on Fridays but no other days.
    #Lunch can be the same every day, but breakfast should not be
    #Should try to have at least 1 drink a day but can have 2 or 0
    #Breakfast isn't required, nor are snacks, but one or the other is required
    #Daily calorie intake should not be exceded by more than 100
    #  
    days = []


    for day in DayName:
        #make a new day
        day = Day(day)
        #we start with breakfast
        #if it's a thursday or sunday I tend to want breakfast
        if day.name == DayName.Thursday or day.name == DayName.Sunday:
            day.breakfast = random.choice(meals.breakfast)
            day.calcount = day.breakfast.calories
        #now I need to put the highest cal meal to help make choices for lunch
        #and make choices for snacks
        #since I don't want to repeat Dinners, I'll pop it
        rngdinner = random.choice(meals.dinner)
        day.dinner = rngdinner
        meals.dinner.remove(rngdinner)
        day.calcount += day.dinner.calories
        #now to check if it's a day for booze
        if day.name == DayName.Wednesday or day.name == DayName.Friday:
            day.liquor = random.choice(meals.liquor)
            day.calcount += day.liquor.calories
        #Time to add in a n/a drink for the day
        rngdrink = random.choice(meals.drink)
        day.drink.append(rngdrink)
        day.calcount += rngdrink.calories
        #Now to figure out lunch
        day.lunch = add_lunch(cal,day,meals.lunch)
        
        calleft = cal - day.calcount
        snacks = meals.snack.copy()
        drinks = meals.drink.copy()
        while(calleft != None):
            if calleft == 0:
                calleft = None
            #we should always have a drink at this point,
            #and can check if it's cool to add snacks
            if len(day.snack) <= 1:
                calleft = cal - day.caltotal
                for snack in snacks.copy():
                    if snack.calories >= calleft:
                        snacks.remove(snack)
                try:
                    assert snacks, "Snacks is empty, can not add stack"
                    day.snack.append(random.choice(snacks))
                    calleft = cal - day.calcount

                except AssertionError as e:
                    #print("Update: ",str(e))
                    pass
                
            #now that we've added snacks time to add drinks
            for drink in drinks.copy():
                if drink.calories >= calleft:
                    drinks.remove(drink)

            
            try:
                assert drinks, "No more drinks, droping the loop"
                day.drink.append(random.choice(drinks))
                calleft = day.calcount - cal
            except AssertionError as e:
                calleft = None
            print('added')

        print(str(day.caltotal) + " " + str(day.name))

        days.append(day)

    data = []
    for day in days:
        snacksjoin = ""
        for snack in day.snack:
            snacksjoin += str(snack.name) + " "
        drinksjoin = ""
        for drink in day.drink:
            drinksjoin += str(drink.name) + " "

        data.append({
        "Day": str(day.name)[len("DayName."):] if str(day.name).startswith("DayName.") else str(day.name),
        "Breakfast": day.breakfast,
        "Lunch": day.lunch,
        "Dinner": day.dinner,
        "Snack": snacksjoin,
        "Drinks": drinksjoin,
        "Liquor": day.liquor,
        "CalorieCount": day.caltotal
    })
    frame = pd.DataFrame(data)
    frame.to_excel("meals.xlsx", index=False)




def add_lunch(cal,day,lunches):
     #Now to figure out lunch
        calleft = cal - day.caltotal

        try:
            #First we need to make sure that we have calories left for lunch
            #if we don't at this point something has gone wrong
            assert calleft >= 0, "You've hit 0 by lunch, something has gone wrong \n not adding lunch!"
            #next we check to make sure that any of the lunches will work 
            #and remove those that won't fit in the budget
            
            toremove = []
            for lunch in lunches:
                if lunch.calories >= calleft:
                    toremove.append(lunch)
            assert len(toremove) != len(lunches), "No lunch works! Something has gone wrong!!!"
            #assuming we have lunches left that work
            if toremove:
                for lunch in toremove:
                    lunches.remove(lunch)
            #sanity check
            assert lunches, "Somehow no lunch is workiong?! Something borked"

            lunch = random.choice(lunches)
            calleft = cal - (day.caltotal + lunch.calories)
            #sanity check
            assert calleft >= 0, "You've hit 0 after lunch"
            return lunch
            


        except AssertionError as e:
            print("Error",str(e))
            return
        
    

    

if __name__ == "__main__":
    main()

    
    






