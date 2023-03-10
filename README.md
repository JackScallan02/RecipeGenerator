# RecipeGenerator
Web application that retrieves a random recipe from Spoonacular given user constraints via RapidAPI. Uses Flask to retrieve and process user inputs.


## Application Details
The user is able to enter in their macronutrient preferences, including minimum/maximum protein and calories, and maximum sodium and sugar. If no recipe is found, the user is notified and they must modify their constraints. Fields left empty will auto-fill under the assumption that the user has no preference for that respective field.

## Technology Details
In the web application, I use Flask to obtain the user macronutrient entries from a POST request via an HTML form. Then, the entries get checked for validation, and we retrieve the recipe.

A python script called `getrecipe.py` contains methods that retrieve the recipe information from Spoonacular. It uses an API key stored in an environment variable to send GET requests to RapidAPI. The first request obtains a list of all recipes that fit within the macronutrient constraints. Then, a random recipe is chosen from that list, and using its ID, we retrieve that recipe's information using another request.

Finally, upon retrieval of the recipe, I utilized Jinja2 to display the recipe information to the user, including the image, link to the website, required ingredients and their respective quantities, and step-by-step instructions.
