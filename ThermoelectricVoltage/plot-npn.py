import matplotlib.pyplot as plt 
import pandas as pd 

datas = pd.read_csv("testing-MOSFET.csv")

x = datas["Gate_Voltage"]
y = datas["Drain_Current"] * 1000

plt.plot(x, y)
plt.xlabel("Gate voltage (V)")
plt.ylabel("Drain Current (mA)")
plt.show()