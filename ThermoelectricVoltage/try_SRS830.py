from pymeasure.instruments.srs import SR830
import time
import csv

srs = SR830("GPIB0::10")            # Set SR830 GPIB address
srs.reference_source = 'Internal'   # Set the reference source
srs.sensitivity = 100e-6            # Set the sensitivity
srs.sine_voltage = 0.375            # Set the voltage ampititube
srs.time_constant = 1e-3            # Set the time constance
srs.input_coupling = 'AC'           # Set the input coupling
srs.filter_synchronous = True       # Ture on the sychronout filter
srs.channel1 = "X"                  # Set channel_1 data display
srs.channel2 = "Theta"              # Set channel_2 data display

srs.trigger_by_bus()                # Set the trigger mode
srs.reset_buffer()                  # Reset the buffer data
srs.start()                         # Init buffer

size_max = 9                        # Set the buffer size, start from 0        
while srs.buffer_counter <= size_max:                   # Buffer point less then maximum size, loop continuous
    srs.trigger()                   # Trigger the buffer storage
    time.sleep(1)                   # Sleep for 1 second
    print("Data buffer counter: ", srs.buffer_counter)
srs.pause_buffer()                  # Pauses data storage
datas = srs.get_datas(1, 0, size_max+1)   # Read the data from buffer
print(datas)
fileName = "Data/LockIn/tc1.csv"
with open(fileName, 'a', newline='') as csvfile:
    header = ["Timestamp", "Temperature", "Voltage"]
    writer = csv.DictWriter(csvfile, fieldnames=header)
    if csvfile.tell() == 0:
        writer.writeheader()
    index = 0
    while index <= size_max:
        writer.writerow(
            {
                # "Timestamp": now,
                # "Temperature": temp,
                "Voltage": datas[index]
            }
        )
        index += 1
csvfile.close()

srs.reset_buffer()                  # Clear the data from buffer