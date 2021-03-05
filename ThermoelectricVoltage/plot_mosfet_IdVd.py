import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np

datas = pd.read_csv("testing-MOSFET_IdVd.csv")
points = 11
index = 0
x_datas = []
y_datas = []

x_conductaces = []
y_conductaces = []

print(len(datas))

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('MOSFET Characteristic')

while index <= len(datas):
    x_datas.append(datas["Drain_Voltage"][index:index+points])
    y_datas.append(datas["Drain_Current"][index:index+points])
    index += points

index_conductance = 0
while index_conductance <= len(datas)-1:
    x_conductaces.append(datas["Gate_Voltage"][index_conductance])
    y_conductaces.append((datas["Drain_Current"][index_conductance+10] - datas["Drain_Current"][index_conductance]) / (datas["Drain_Voltage"][index_conductance+10] - datas["Drain_Voltage"][index_conductance]))

    index_conductance += points
print(x_conductaces, y_conductaces)
index_plot = 0
while index_plot <= len(datas)/points-1:
    ax1.plot(x_datas[index_plot], y_datas[index_plot], label="{}".format(datas["Gate_Voltage"][(points)*index_plot]))
    ax1.legend()
    # ax1.xlabel("Drain Voltage")
    index_plot += 1

ax2.plot(x_conductaces, y_conductaces)

plt.show()