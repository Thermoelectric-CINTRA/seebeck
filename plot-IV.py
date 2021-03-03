import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from scipy import optimize
from numpy import arange


def objective(x, a, b):
    return a*x**2+ b


datas = pd.read_csv("ac-tc1-tc2.csv")
# x = datas['HeaterCurrent']
x = datas['HeaterCurrent']
y = datas['Vtc1']/3.024e-6
y2 = datas['Vtc2']/3.024e-6

# curve fit
popt, _ = curve_fit(objective, x, y)
popt_2, _ = curve_fit(objective, x, y2)

# summarize the parameter values
a, b = popt
a1, b1 = popt_2
print('y1 = %.5f * x + %.5f' % (a, b))
print('y2 = %.5f * x + %.5f' % (a1, b1))

# define a sequence of inputs between the smallest and largest known inputs
x_line = x
# calculate the output for the range
y_line = objective(x_line, a, b)
y2_line = objective(x_line, a1, b1)


fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Resistance TC1 & TC2 at 450 K')
ax1.plot(x, y, 'r', label="TC1")
ax2.plot(x, y2, 'b', label="TC2")
fig.text(0.5, 0.04, 'I heater (mA)', ha='center')
fig.text(0.04, 0.5, 'R (Ohm)', va='center', rotation='vertical')
ax1.legend()
ax2.legend()
# create a line plot for the mapping function
ax1.plot(x_line, y_line, '--', color='red')
ax2.plot(x_line, y2_line, '--', color='blue')

plt.show()