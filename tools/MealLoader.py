import json

def MealLoader(path):
    with open(path, 'r') as file:
        json_data = file.read()
    
    meals = []

    for line in json_data.split('\n'):
        if line.strip():
            json_object = json.loads(line)
            meals.append(json_object)
    return meals