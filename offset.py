from pymeasure.instruments.keithley import Keithley2000
from pymeasure.instruments.lakeshore import LakeShore330
import csv
import time
from datetime import datetime

lakeshore = LakeShore330("GPIB0::5")
volmeter = Keithley2000("GPIB0::3")

while True:
    Timestamp = datetime.now().time()
    fileName = "offset.csv"
    with open(fileName, 'a', newline='') as csvfile:
        header = ["Timestamp", "Temperature", "Voltage"]
        writer = csv.DictWriter(csvfile, fieldnames=header)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(
            {
                "Timestamp": Timestamp,
                "Temperature": lakeshore.temperature_A,
                "Voltage": volmeter.voltage
            }
        )
    csvfile.close()
    time.sleep(0.5)