from pymeasure.instruments.keithley import Keithley2000

def ThermoelectricVoltage():
    # Connect to keithley 2000 multimeter
    voltage = Keithley2000("GPIB0::3")
    # 
    READING = voltage.datas()
    
    return READING

Reading = ThermoelectricVoltage()
print(Reading)