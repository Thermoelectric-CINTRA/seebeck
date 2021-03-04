import matplotlib.pyplot as plt 
import pandas as pd 

datas = pd.read_csv("testing-npn.csv")

x = datas["Base_Voltage"]
y = datas["BE_Current"] * 1000

plt.plot(x, y)
plt.xlabel("Base voltage (V)")
plt.ylabel("Base Current (mA)")
plt.show()