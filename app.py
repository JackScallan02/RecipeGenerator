from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import json
from getrecipe import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = "super secret key"
db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        minProtein = request.form['minProtein']
        maxProtein = request.form['maxProtein']
        minCalories = request.form['minCalories']
        maxCalories = request.form['maxCalories']
        maxSodium = request.form['maxSodium']
        maxSugar = request.form['maxSugar']

        macros = {"minProtein": minProtein, "maxProtein": maxProtein,
        "minCalories": minCalories, "maxCalories": maxCalories,
        "sodium": maxSodium, "sugar": maxSugar}

        if not validateMacros(macros):
            print("Invalid macros")
            return render_template('index.html',visibility="visible")
        else:
            id = getMealID(macros)
            title = ""
            img = ""
            url = ""
            ingredientNameList = []
            ingredientQuantityList = []
            instructionsList = []

            if id == -1: #Recipe was unable to be found
                recipe = json.dumps({"title": title, "img":img, "ingredients": {"name":ingredientNameList, "quantity":ingredientQuantityList}, "instructions":instructionsList, "url":url})
            else:
                response = getRecipeInfo(id)
                title = response["title"]
                img = response["image"]
                ingredients = response["extendedIngredients"]
                url = response["sourceUrl"]

                for i in range(len(ingredients)):
                    ingredientNameList.append(ingredients[i]["name"])
                    ingredientQuantityList.append(str(ingredients[i]["amount"]) + " " + ingredients[i]["unit"])

                if (response["analyzedInstructions"]):
                    instructions = response["analyzedInstructions"]
                    steps = response["analyzedInstructions"][0]["steps"]

                    for i in range(len(steps)):
                        instructionsList.append(steps[i]["step"])
                else:
                    print("No steps are supported for this recipe.")



            recipe = json.dumps({"title": title, "img":img, "ingredients": {"name":ingredientNameList, "quantity":ingredientQuantityList}, "instructions":instructionsList, "url":url})

            session['recipe'] = recipe
            return redirect(url_for('.showRecipe', recipe=recipe))

    else:
        return render_template('index.html',visibility="hidden")




@app.route('/recipe')
def showRecipe():
    recipe = session['recipe']
    return render_template('recipe.html', recipe=json.loads(recipe))


if __name__ == "__main__":
    app.run(debug=True)
