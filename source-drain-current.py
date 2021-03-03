from pymeasure.instruments.keithley import Keithley2400
# from pymeasure.instruments.keithley import Keithley2420
import time
import csv

vd = Keithley2400("GPIB0::6")
# vg = Keithley2400("GPIB0::8")

vd.source_voltage = 0
vd.enable_source()
vd.measure_current()

drain = -5
while drain <= 5:
    vd.source_voltage = drain
    # vd.enable_source()
    # vg.measure_voltage()
    fileName = "source-drain-current.csv"
    with open(fileName, 'a', newline='') as csvfile:
        header = ["Vg", "Current"]
        writer = csv.DictWriter(csvfile, fieldnames=header)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(
            {
                "Vg": drain,
                "Current": vd.current
            }
        )
    csvfile.close()
    drain += 0.1
    # vg.disable_source()
    time.sleep(1)

# GateVoltage = -70
# while GateVoltage <= 70:
#     vg.source_voltage = GateVoltage
#     vg.enable_source()
#     # vg.measure_voltage()
#     fileName = "source-drain-current.csv"
#     with open(fileName, 'a', newline='') as csvfile:
#         header = ["Vg", "Current"]
#         writer = csv.DictWriter(csvfile, fieldnames=header)
#         if csvfile.tell() == 0:
#             writer.writeheader()
#         writer.writerow(
#             {
#                 "Vg": GateVoltage,
#                 "Current": vd.current
#             }
#         )
#     csvfile.close()
#     GateVoltage += 5
#     # vg.disable_source()
#     time.sleep(5)
# vg.source_mode = "voltage"
# vg.compliance_current = 1
# vg.source_voltage = -5
# vg.auto_range_source()
# vg.enable_source()
# vg.measure_voltage()
# print(vg.voltage_range)