# RecipeGenerator
Web application that retrieves a random recipe from Spoonacular given user constraints via RapidAPI. Uses Flask to retrieve and process user inputs.


## Application Details
The user is able to enter in their macronutrient preferences, including minimum/maximum protein and calories, and maximum sodium and sugar. If no recipe is found, the user is notified and they must modify their constraints. Fields left empty will auto-fill under the assumption that the user has no preference for that respective field.

Additionally, a user can click on the "get suggestion" button and it will generate a random recipe based on past user macronutrient preferences by using machine learning.

## Technology Details
In the web application, I use Flask to obtain the user macronutrient entries from a POST request via an HTML form. Then, the entries get checked for validation, and we retrieve the recipe.

A python script called `getrecipe.py` contains methods that retrieve the recipe information from Spoonacular. It uses an API key stored in an environment variable to send GET requests to RapidAPI. The first request obtains a list of all recipes that fit within the macronutrient constraints. Then, a random recipe is chosen from that list, and using its ID, we retrieve that recipe's information using another request.

Finally, upon retrieval of the recipe, I utilized Jinja2 to display the recipe information to the user, including the image, link to the website, required ingredients and their respective quantities, and step-by-step instructions.

To get a suggested recipe, I utilized Scikit-learn to implement linear regression by reading from a csv file using Pandas, which contains past user ratings. For example, if a user rated a recipe a 5, the csv file would contain the macronutrient information as well as the rating.
