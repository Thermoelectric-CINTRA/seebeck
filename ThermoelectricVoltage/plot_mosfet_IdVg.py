import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np

datas = pd.read_csv("testing-MOSFET_IdVg.csv")

index = 0
x_datas = []
y_datas = []
print(len(datas))
while index <= len(datas):
    x_datas.append(datas["Gate_Voltage"][index:index+10])
    y_datas.append(datas["Drain_Current"][index:index+10])
    index += 10

index2 = 0
while index2 <= len(datas)/10:
    plt.plot(x_datas[index2], y_datas[index2], label="{}".format(datas["Drain_Voltage"][index2+10]))
    index2 += 1

plt.xlabel("Gate voltage (V)")
plt.ylabel("Drain Current (A)")
plt.legend()
plt.show()