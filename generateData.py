import csv
import random
import numpy as np


'''
We want to generate 100000 data points.
90000 will be normally distributed with mean [15, 50, 300, 600, 20, 300] and variance 1.
10000 will be randomly distributed.
'''

with open('preferences.csv', mode='w', newline='') as f:
    writer = csv.writer(f, delimiter=',')

    #Generate 90% normally distributed data
    #minProtein, maxProtein, minCalories, maxCalories, maxSugar, maxSodium
    mu = [15, 50, 300, 600, 20, 300]
    sigma = np.ones(6)

    data = np.random.normal(loc=mu, scale=sigma, size=(90000, 6)).astype(int)
    for row in data:
        writer.writerow(np.append(row, random.randint(3, 5)))

    data = []
    for i in range(10000):
        data.append([random.randint(0, 50), random.randint(20, 70), random.randint(0, 700), random.randint(100, 2000), random.randint(10, 70), random.randint(300, 2000), random.randint(1, 5)])

    #Generate 10% random data
    for row in data:
        writer.writerow(row)
