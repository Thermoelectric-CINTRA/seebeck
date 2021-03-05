import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np

# datas = pd.read_csv("testing-MOSFET.csv")

# index = 0
# x1 = datas["Drain_Voltage"][index:index+51]
# y1 = datas["Drain_Current"][index:index+51] * 1000
# y1_log = np.log(y1)

# x2 = datas["Drain_Voltage"][index+52:index+51*2]
# y2 = datas["Drain_Current"][index+52:index+51*2] * 1000
# y2_log = np.log(y2)

# x3 = datas["Drain_Voltage"][index+52*2:index+51*3]
# y3 = datas["Drain_Current"][index+52*2:index+51*3] * 1000
# y3_log = np.log(y3)

# x4 = datas["Drain_Voltage"][index+52*3:index+51*4]
# y4 = datas["Drain_Current"][index+52*3:index+51*4] * 1000
# y4_log = np.log(y4)

# x5 = datas["Drain_Voltage"][index+52*4:index+51*5]
# y5 = datas["Drain_Current"][index+52*4:index+51*5] * 1000
# y5_log = np.log(y5)

# x6 = datas["Drain_Voltage"][index+52*5:index+51*6]
# y6 = datas["Drain_Current"][index+52*5:index+51*6] * 1000
# y6_log = np.log(y6)

# x7 = datas["Drain_Voltage"][index+52*6:index+51*7]
# y7 = datas["Drain_Current"][index+52*6:index+51*7] * 1000
# y7_log = np.log(y7)

# plt.plot(x1, y1_log, label="Vg=4.5")
# plt.plot(x2, y2_log, label="Vg=4")
# plt.plot(x3, y3_log, label="Vg=3.5")
# plt.plot(x4, y4_log, label="Vg=3")
# plt.plot(x5, y5_log, label="Vg=2.5")
# plt.plot(x6, y6_log, label="Vg=2")
# plt.plot(x7, y7_log, label="Vg=1.5")

datas = pd.read_csv("testing-MOSFET_IdVg.csv")

index = 0
x1 = datas["Gate_Voltage"][index:index+101]
y1 = datas["Drain_Current"][index:index+101] * 1000
y1_log = np.log(y1)

x2 = datas["Gate_Voltage"][index+102:index+101*2]
y2 = datas["Drain_Current"][index+102:index+101*2] * 1000
y2_log = np.log(y2)

plt.plot(x1, y1, label="Vd=0.5")
plt.plot(x2, y2, label="Vd=1")

plt.xlabel("Gate voltage (V)")
plt.ylabel("Drain Current (mA)")
plt.legend()
plt.show()