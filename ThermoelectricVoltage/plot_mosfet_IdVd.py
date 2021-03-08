import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np
from scipy.optimize import curve_fit

datas = pd.read_csv("Data/MOSFET/2021-03-07/MOSFET_IdVd_8.csv")
points = 11
index = 0
x_datas = []
y_datas = []

x_conductaces = []
y_conductaces = []

print(len(datas))

def objective(x, a, b):
    return a * x + b

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('MOSFET Characteristic')

while index <= len(datas):
    x_datas.append(datas["Drain_Voltage"][index:index+points])
    y_datas.append(datas["Drain_Current"][index:index+points])
    index += points

index_conductance = 0
while index_conductance <= len(datas)-1:
    x_conductaces.append(datas["Gate_Voltage"][index_conductance])
    y_conductaces.append((datas["Drain_Current"][index_conductance+10] - datas["Drain_Current"][index_conductance+5]) / (datas["Drain_Voltage"][index_conductance+10] - datas["Drain_Voltage"][index_conductance+5]))
    index_conductance += points
print(x_conductaces, y_conductaces)
index_plot = 0
while index_plot <= len(datas)/points-1:
    ax1.plot(x_datas[index_plot], y_datas[index_plot], label="Vg={}V".format(datas["Gate_Voltage"][(points)*index_plot]))
    ax1.legend(ncol=2)
    index_plot += 1

# curve fit
popt, _ = curve_fit(objective, x_conductaces[19:23], y_conductaces[19:23])
# summarize the parameter values
a, b = popt
print('y = %.5f * x + %.5f' % (a, b))

ax1.set_xlabel("Drain Voltage Vd(V)")
ax1.set_ylabel("Drain Current Id(A)")
ax2.plot(x_conductaces, y_conductaces)

# define a sequence of inputs between the smallest and largest known inputs
# x_line = np.arange(min(x_conductaces), max(x_conductaces))
x_line = np.arange(-b/a, 2.5, 0.1)
# calculate the output for the range
y_line = objective(x_line, a, b)
print("x line: ", x_line)
print("y line: ", y_line)
# create a line plot for the mapping function
ax2.plot(x_line, y_line, '--', color='red')
ax2.text(2.2, 1, 'y = %.5f * x + (%.5f)' % (a, b))
ax2.text(2.2, 0.8, "Vth = {}".format(-b/a))

ax2.set_xlabel("Gate Voltage Vg(V)")
ax2.set_ylabel("Conductance G(S)")
plt.show()