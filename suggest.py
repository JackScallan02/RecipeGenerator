import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import requests
import os
from getrecipe import *
import time





def getRandomRecipe():
    #Returns id of a random recipe
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/random"
    querystring = {"number":"1"}
    headers = {
	"X-RapidAPI-Key": os.environ.get("APIKEY"),
	"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if (response.status_code != 200):
        print("Invalid request; status code:", response.status_code)
        return -1


    id=response.json()["recipes"][0]["id"]
    return id

def getMacrosFromRecipe(id):
    #Return the macros from a recipe id

    #Get response object from method defined in getrecipe.py
    response = getRecipeInfo(id)
    nutrients = response["nutrition"]["nutrients"]

    macros = []
    macros.append(round(nutrients[8]["amount"])) #Protein
    macros.append(round(nutrients[0]["amount"])) #Calories
    macros.append(round(nutrients[5]["amount"])) #Sugar
    macros.append(round(nutrients[7]["amount"])) #Sodium
    return macros

def getModel():
    df = pd.read_csv("ratings.csv", sep=",", header=None)
    X = df.iloc[:, 0:4]
    y = df.iloc[:, 4]

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model


def suggestRecipe(macros, id):
    #Repeatedly retrieve a random recipe from API and fit to model to check rating prediction
    model = getModel()
    rating = round(model.predict([macros])[0])
    while rating < 4:
        print("Rating < 4. Regenerating.")
        id = getRandomRecipe()
        macros = getMacrosFromRecipe(id)

        rating = round(model.predict([macros])[0])
        time.sleep(2)

    return id

    #Gets the predicted user rating given a recipe




#id = getRandomRecipe()
#macros = getMacrosFromRecipe(id)
#newID = suggestRecipe(macros, id)

#mse = mean_squared_error(y_test, y_prediction)
#rmse = np.sqrt(mse)
#rmspe = rmse / np.mean(y_test) * 100

#print(rmspe)
