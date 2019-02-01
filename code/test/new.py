import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('/home/pi/test/change.csv')
#data['balance'] = [300,200,100]
name = np.array(data['name'])
balance = np.array(data['balance'])
print(balance)
found_index = [code for code in range(len(data['tag']))  if data.iloc[code,1] == "0900711DDFBA"]
user_name = data.iloc[found_index, 0]
user_balance = data.iloc[found_index, 2]
print("tag matched for {}, the balance is: {}".format(user_name[0], user_balance[0]))
data.iloc[found_index,2] = user_balance - 20
new_balance = data.iloc[found_index, 2]
data.to_csv('/home/pi/test/change.csv', index = False) # to write the data back to the csv file(updation without index)
print("the new balance of {} : {}".format(user_name[0], new_balance[0]))  
print(data.head())

data['balance'].plot(kind = 'hist', bins = 20)
plt.xlabel('names')
plt.show()
