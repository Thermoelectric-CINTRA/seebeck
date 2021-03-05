from pymeasure.instruments.keithley import Keithley2000
from pymeasure.instruments.keithley import Keithley2420
from pymeasure.instruments.keithley import Keithley2400
import time
import csv
gatevoltage = Keithley2400("GPIB0::8")
vce = Keithley2420("GPIB0::6")
gatevoltage.measure_current()
vce.measure_current()
voltage = 0
while voltage <= 150:
    gatevoltage.source_voltage = voltage
    vce.source_voltage = 0.5
    fileName = "testing-MOSFET.csv"
    with open(fileName, 'a', newline='') as csvfile:
        header = ["Gate_Voltage", "Gate_Current","Drain_Voltage", "Drain_Current"]
        writer = csv.DictWriter(csvfile, fieldnames=header)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(
            {
                "Gate_Voltage": voltage,
                "Gate_Current": gatevoltage.current,
                "Drain_Voltage": vce.source_voltage,
                "Drain_Current": vce.current
            }
        )
    csvfile.close()
    time.sleep(1)
    voltage += 1

# voltage = 0
# while voltage <= 5:
#     vce.source_voltage = voltage
#     fileName = "testing-npn.csv"
#     with open(fileName, 'a', newline='') as csvfile:
#         header = ["Base_Voltage", "BE_Current","CE_Voltage", "CE_Current"]
#         writer = csv.DictWriter(csvfile, fieldnames=header)
#         if csvfile.tell() == 0:
#             writer.writeheader()
#         writer.writerow(
#             {
#                 "Base_Voltage": voltage,
#                 "BE_Current": gatevoltage.current,
#                 "CE_Voltage": vce.source_voltage,
#                 "CE_Current": vce.current
#             }
#         )
#     csvfile.close()
#     time.sleep(1)
#     voltage += 0.1
