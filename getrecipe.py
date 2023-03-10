import requests
import random
import os

'''
This script contains methods for retrieving recipes from Spoonacular.
From the API, the script uses "Get Recipe Information" and "Search Recipes by Nutrients".

pip install -r requirements.txt to install requirements.
'''


def validateMacros(macros):
    #Ensures that the user enters in integers.
    #If the user leaves a field blank, autofill it with a value.
    valid = True
    for macro in macros:
        if macros[macro] == "":
            if macro in {"minProtein", "minCalories"}:
                macros[macro] = 0
            else:
                macros[macro] = 100000
        elif macros[macro].isdigit():
            macros[macro] = int(macros[macro])
        else:
            #Not a valid input, return False
            valid = False
            macros[macro] = False

    return valid


def getMealID(macros):
    #Returns the ID of a random meal that fits the macro requirements.
    #Returns False if unable to get a meal.
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByNutrients"
    querystring = {"limitLicense":"false","minProtein":macros["minProtein"],"maxProtein":macros["maxProtein"],
    "minCalories":macros["minCalories"],"maxCalories":macros["maxCalories"],"maxSodium":macros["sodium"],
    "maxSugar":macros["sugar"]}
    headers = {
	"X-RapidAPI-Key": os.environ.get("APIKEY"),
	"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    if (response.status_code != 200):
        print("Invalid request; status code:"
        , response.status_code)
        print("Try changing your macro requirements.\n")
        return False

    id = -1
    try:
        randomRecipe = random.randint(0, len(response.json()) - 1)
        id=response.json()[randomRecipe]["id"]
    except:
        print("No recipe was found")

    return id




def getRecipeInfo(id):
    #Retrieves the ingredients and instructions for the recipe
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/" + str(id) + "/information"

    querystring = {"includeNutrition":"true"}

    headers = {
	   "X-RapidAPI-Key": os.environ.get("APIKEY"),
	   "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()

    print(response)

    return response




def displayRecipeInfo(response):
    title = response["title"]
    print("RECIPE TITLE: ", title, "\n")

    image = response["image"]

    ingredients = response["extendedIngredients"]
    for i in range(len(ingredients)):
        print("Ingredient: ", ingredients[i]["name"], ", Quantity: ", ingredients[i]["amount"], " ", ingredients[i]["unit"])


    if (response["analyzedInstructions"]):
        steps = response["analyzedInstructions"][0]["steps"]

        for i in range(len(steps)):
            print("Step ", i, ": ", steps[i]["step"])
    else:
        print("No steps are supported for this recipe.")
