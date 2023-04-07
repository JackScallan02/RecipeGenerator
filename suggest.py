import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import statistics



df = pd.read_csv("preferences.csv", sep=",")

X = df.iloc[:, 0:6]
y = df.iloc[:, 6]

X_train, X_test, y_train, y_test = train_test_split(X, y)

model = LinearRegression()
model.fit(X_train, y_train)

y_prediction = model.predict(X_test)

#mse = mean_squared_error(y_test, y_prediction)
#rmse = np.sqrt(mse)
#rmspe = rmse / np.mean(y_test) * 100
#print(round(model.predict([[15, 50, 300, 600, 20, 300]])[0]))
#print(rmspe)
