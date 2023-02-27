import requests
import random
import pandas as pd

#Uses "Get Recipe Information" and "Search Recipes by Nutrients"

def getValidMacroFromUser(question, constraints):
    #Prompts user with question and makes sure they enter a number within given constraints
    macro = input(question)
    while not macro.isdigit() or int(macro) < constraints[0] or int(macro) > constraints[1]:
        if not macro.isdigit():
            print("Please enter an integer.")
        else:
            print("Please enter a number in a reasonable range (", str(constraints[0]), " to ", str(constraints[1]), ")")
        macro = input(question)

    return macro


def prompt():
    #Prompts the user for macro preferences
    print("Input your following preferences on a serving-basis.")

    proteinMinInput = getValidMacroFromUser("What minimum amount of protein would you like?: ", [0, 100])
    proteinMaxInput = getValidMacroFromUser("What maximum amount of protein would you like?: ", [0, float("inf")])
    caloriesMinInput = getValidMacroFromUser("What minimum amount of calories would you like?: ", [0, 4000])
    caloriesMaxInput = getValidMacroFromUser("What maximum amount of calories would you like?: ", [0, float("inf")])
    sodiumInput = getValidMacroFromUser("What maximum amount of sodium would you like?: ", [0, float("inf")])
    sugarInput = getValidMacroFromUser("What maximum amount of sugar would you like?: ", [0, float("inf")])


    #proteinMinInput = 0
    #proteinMaxInput = 70
    #caloriesMinInput = 300
    #caloriesMaxInput = 1000
    #sodiumInput = 800
    #sugarInput = 40

    #Do error checking
    return {"minProtein": proteinMinInput, "maxProtein": proteinMaxInput,
    "minCalories": caloriesMinInput, "maxCalories": caloriesMaxInput,
    "sodium": sodiumInput, "sugar": sugarInput}



def getMealID(macros):
    #Returns the ID of a random meal that fits the macro requirements
    #Returns False if unable to get a meal
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByNutrients"
    querystring = {"limitLicense":"false","minProtein":macros["minProtein"],"maxProtein":macros["maxProtein"],
    "minCalories":macros["minCalories"],"maxCalories":macros["maxCalories"],"maxSodium":macros["sodium"],
    "maxSugar":macros["sugar"]}
    headers = {
	"X-RapidAPI-Key": "",
	"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    if (response.status_code != 200):
        print("Invalid request; status code:", response.status_code)
        print("Try changing your macro requirements.\n")
        return False

    randomRecipe = random.randint(0, len(response.json()) - 1)
    id=response.json()[randomRecipe]["id"]
    return id


def getRecipeInfo(id):
    #Retrieves the ingredients and instructions for the recipe
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/" + str(id) + "/information"

    querystring = {"includeNutrition":"true"}

    headers = {
	   "X-RapidAPI-Key": "",
	   "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()

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



def main():
    id = False
    while id == False:
        macros = prompt()
        id = getMealID(macros)

    response = getRecipeInfo(id)
    displayRecipeInfo(response)



if __name__ == '__main__':
    main()
