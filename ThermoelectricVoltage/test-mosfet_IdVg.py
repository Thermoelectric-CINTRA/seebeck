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
drainvoltage = 0
gatevoltage = 2.2
while gatevoltage <= 3:
    gate.source_voltage = gatevoltage
    while drainvoltage <= 2.5:
        drain.source_voltage = drainvoltage
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
        drainvoltage += 0.5
    
    gatevoltage += 0.2
    rainvoltage = 0
    time.sleep(1)

gate.source_voltage = 0
drain.source_voltage = 0
