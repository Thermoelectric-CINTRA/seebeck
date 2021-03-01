import matplotlib.pyplot as plt
import pandas as pd

datas = pd.read_csv("IV-4.csv")
x = datas['Current']
y = datas['Voltage']
plt.title('IV Curve')
plt.plot(x, y)
plt.show()