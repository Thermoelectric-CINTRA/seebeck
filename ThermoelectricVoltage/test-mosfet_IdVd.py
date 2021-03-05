from pymeasure.instruments.keithley import Keithley2000
from pymeasure.instruments.keithley import Keithley2420
from pymeasure.instruments.keithley import Keithley2400
import time
import csv
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np

gate = Keithley2400("GPIB0::8")
drain = Keithley2420("GPIB0::6")
gate.measure_current()
drain.measure_current()
drainvoltage_min = -0.5
drainvoltage_max = 0.5
gatevoltage = 0
while gatevoltage <= 3:
    gate.source_voltage = gatevoltage
    while drainvoltage_min <= drainvoltage_max:
        drain.source_voltage = drainvoltage_min
        fileName = "testing-MOSFET_IdVd.csv"
        with open(fileName, 'a', newline='') as csvfile:
            header = ["Gate_Voltage", "Gate_Current","Drain_Voltage", "Drain_Current"]
            writer = csv.DictWriter(csvfile, fieldnames=header)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(
                {
                    "Gate_Voltage": gate.source_voltage,
                    "Gate_Current": gate.current,
                    "Drain_Voltage": drain.source_voltage,
                    "Drain_Current": drain.current
                }
            )
        csvfile.close()
        time.sleep(1)
        drainvoltage_min += 0.1
        print("Drain Voltage: ", drainvoltage_min)
    gatevoltage += 0.2
    print("Gate Voltage: ", gatevoltage)
    drainvoltage_min = -0.5 # Drain Voltage Reset Point
    time.sleep(1)

gate.source_voltage = 0
drain.source_voltage = 0

# datas = pd.read_csv("testing-MOSFET_IdVd.csv")
# points = 11
# index = 0
# x_datas = []
# y_datas = []
# print(len(datas))
# while index <= len(datas):
#     x_datas.append(datas["Drain_Voltage"][index:index+points])
#     y_datas.append(datas["Drain_Current"][index:index+points])
#     index += points
# index_plot = 0
# while index_plot <= len(datas)/points-1:
#     plt.plot(x_datas[index_plot], y_datas[index_plot], label="{}".format(datas["Gate_Voltage"][(points)*index_plot]))
#     index_plot += 1

# plt.xlabel("Drain voltage (V)")
# plt.ylabel("Drain Current (A)")
# plt.legend()
# plt.show()