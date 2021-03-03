import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from scipy import optimize
from numpy import arange


def objective(x, a, b):
    return a*x**2+ b


datas = pd.read_csv("IV-4.csv")
x = datas['Current']
y = datas['Voltage'] * 1000

# curve fit
popt, _ = curve_fit(objective, x, y)

# summarize the parameter values
a, b = popt
print('y1 = %.5f * x + %.5f' % (a, b))


# define a sequence of inputs between the smallest and largest known inputs
x_line = x
# calculate the output for the range
y_line = objective(x_line, a, b)


plt.plot(x, y, '-', color='red', label="Data")
plt.plot(x, y_line, '--', color='blue', label="Fitting")
plt.xlabel("Heater Current (mA)")
plt.ylabel("Voltage (mV)")
plt.title("Thermoelectric Voltage")
plt.legend()

plt.show()