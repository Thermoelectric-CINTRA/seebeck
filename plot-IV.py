import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from scipy import optimize
from numpy import arange


def objective(x, a, b):
    return a*x**2+ b


datas = pd.read_csv("ac-tc1-tc2.csv")
# x = datas['HeaterCurrent']
x = datas['HeaterCurrent'][0:19]
y = datas['Vtc1'][0:19]/3.024e-6
y2 = datas['Vtc2'][0:19]/3.024e-6

x_300 = datas['HeaterCurrent'][20:40]
y_tc2_300 = datas['Vtc2'][20:40]/3.024e-6

# curve fit
popt, _ = curve_fit(objective, x, y)
popt_2, _ = curve_fit(objective, x, y2)
popt_3, _ = curve_fit(objective, x_300, y_tc2_300)

# summarize the parameter values
a, b = popt
a1, b1 = popt_2
a2, b2 = popt_3
print('y1 = %.5f * x + %.5f' % (a, b))
print('y2 = %.5f * x + %.5f' % (a1, b1))
print('y3 = %.5f * x + %.5f' % (a2, b2))

# define a sequence of inputs between the smallest and largest known inputs
x_line = x
x_line_300 = x_300
# calculate the output for the range
y_line = objective(x_line, a, b)
y2_line = objective(x_line, a1, b1)
y3_line = objective(x_line_300, a2, b2)


fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
fig.suptitle('Resistance TC1 & TC2 at 300/450 K')
ax1.plot(x, y, 'r', label="TC1@450K")

ax2.plot(x, y2, 'b', label="TC2@450k")
ax2.plot(x_300, y_tc2_300, 'black', label="TC2@300K")

ax3.plot(x, y2, 'b', label="TC2@450k")
ax3.plot(x_line, y2_line, '--', color='blue')

ax4.plot(x_300, y_tc2_300, 'black', label="TC2@300K")
ax4.plot(x_line_300, y3_line, '*-', color='green')

fig.text(0.5, 0.04, 'I heater (mA)', ha='center')
fig.text(0.04, 0.5, 'R (Ohm)', va='center', rotation='vertical')

# create a line plot for the mapping function
ax1.plot(x_line, y_line, '--', color='red')
ax2.plot(x_line, y2_line, '--', color='blue')
ax2.plot(x_line_300, y3_line, '*-', color='green')
ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()
plt.show()