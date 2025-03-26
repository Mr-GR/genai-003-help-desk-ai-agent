import pandas as pd 
import matplotlib.pyplot as plt 
import sklearn 
import gym 

df = pd.DataFrame({'A': [1,2,3], 'B': [4,5,6]})
print("Pandas DataFrame:\n", df)

plt.plot([1,2,3],[4,5,6])
plt.title("Test Plot")
plt.show()

from sklearn.linear_model import LinearRegression
model = LinearRegression()
print("SciKit-Learn model:", model)

env = gym.make("CartPole-v1")
print("Gym Environment Created", env)