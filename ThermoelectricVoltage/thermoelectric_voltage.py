from pymeasure.instruments.keithley import Keithley2000

def ThermoelectricVoltage(address="GPIB0::3"):
    # Contruct a multimeter 
    volmeter = Keithley2000(address)
    # Configer multimeter into Voltage:DC
    # Set the maximum measurement voltage
    # Set the buffer point
    # Select the buffer storeage
    # Set the buffer fill control
    # Turn off the countinuous init
    # Put the multimeter into init mode
    # Trigger the multimeter
    # Reading the data from buffer
