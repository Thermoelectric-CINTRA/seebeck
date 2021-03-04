from pymeasure.instruments.keithley import Keithley2000
from pymeasure.instruments.keithley import Keithley2420
from pymeasure.instruments.keithley import Keithley2400

def ThermoelectricVoltage(address="GPIB0::3", size=10):
    # Contruct a multimeter 
    volmeter = Keithley2000(address)
    # volmeter.measure_voltage_dc()
    # print(volmeter.mode)
    # Configer multimeter into Voltage:DC
    # Set the maximum measurement voltage
    # clear buffer
    volmeter.clear_buffer()
    # Set the buffer point
    volmeter.buffer_size(size)
    # Select the buffer storeage
    volmeter.buffer_storage()
    # Set the buffer fill control
    volmeter.buffer_control()
    # Turn off the countinuous init
    volmeter.init()
    # Put the multimeter into init mode
    # Trigger the multimeter
    # Reading the data from buffer
    datas = volmeter.datas()
    print(datas)

def HeaterCurrentController(address="GPIB0::6", current=10e-6):
    currentcontroller = Keithley2420(address)
    currentcontroller.source_mode = "current"
    currentcontroller.config_measurement = "Volts"
    currentcontroller.source_current_range = 100e-3
    currentcontroller.compliance_voltage = 3
    currentcontroller.source_current = current

def GateVoltage(address="GPIB0::8", voltage=0):
    gatevoltage = Keithley2400(address)
    gatevoltage.source_mode = "voltage"
    gatevoltage.config_measurement = "Amps"
    gatevoltage.source_voltage_range = 0.8
    gatevoltage.compliance_current = 1
    gatevoltage.source_voltage = voltage


ThermoelectricVoltage()
# HeaterCurrentController()
GateVoltage(voltage=0.3)