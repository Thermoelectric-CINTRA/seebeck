from pymeasure.instruments.nf import LI5640
import time
import csv

nf = LI5640("GPIB0::11")
nf.phase = 0
nf.frequency = 1
# nf.amplitude_50mV = 0.001
nf.amplitude_500mV = 0.375
# nf.amplitude_5V = 2
# nf.harmonic = 1
nf.source = "Int"
nf.edge = "Sine"
nf.signal = "AB"
nf.coupling = "AC"
nf.voltage_sensitivity = 100e-6
nf.time_constant = 30e-3
nf.synchronous = "On"
nf.slope = 24
nf.data1 = "X"
nf.data2 = "Theta"
nf.data_type = "Data1,2"
nf.data_size = "32K"
# nf.data_number = 0
# nf.data_sampling_period = 1
# nf.data_sampling_by_gpib()
# nf.start()
index = 0
data_max = 100
while index <= data_max:
    # nf.trigger()
    fileName = "Data/LockIn/tc2.csv"
    with open(fileName, 'a', newline='') as csvfile:
        header = ["Voltage", "Phase"]
        writer = csv.DictWriter(csvfile, fieldnames=header)
        if csvfile.tell() == 0:
            writer.writeheader()
        datas = nf.read
        writer.writerow(
            {
                "Voltage": datas[0],
                "Phase": datas[1]
            }
        )
    csvfile.close()
    time.sleep(1)
    index += 1

nf.stop()