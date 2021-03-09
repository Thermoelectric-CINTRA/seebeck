from pymeasure.instruments.lakeshore import LakeShore330
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments.hp import HP34401A
from pymeasure.instruments.keysight import Keysight33210A
from pymeasure.instruments.nf import LI5660
from pymeasure.instruments.keithley import Keithley2420
from pymeasure.instruments.keithley import Keithley2000


import csv
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from multiprocessing import Process
import os, os.path
from datetime import datetime as dt
import time

def TempLoop():
    temperatureController = LakeShore330("GPIB0::5")
    second = 0
    date = datetime.date.today()
    DIR = 'Data/temperature/{}'.format(date)
    try:
        os.mkdir(DIR)
    except OSError:
        print ("Creation of the directory %s failed" % DIR)
    else:
        print ("Successfully created the directory %s " % DIR)
    time.sleep(0.1)
    fileNum = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) + 1
    fileName = "Data/temperature/{}/temperature_{}.csv".format(date, fileNum)

    def PID(setpoint):
        if setpoint <= 10:
            temperatureController.gain = 5
            temperatureController.reset = 500
            temperatureController.rate = 0
            temperatureController.heater_range = "medium"
        elif setpoint <= 15 and setpoint > 10:
            temperatureController.gain = 50
            temperatureController.reset = 500
            temperatureController.rate = 0
            temperatureController.heater_range = "medium"
        elif setpoint <= 20 and setpoint > 15:
            temperatureController.gain = 1
            temperatureController.reset = 900
            temperatureController.rate = 0
            temperatureController.heater_range = "high"
        elif setpoint > 20:
            temperatureController.heater_range = "high"
            temperatureController.auto_tune = "PID"
        else:
            temperatureController.heater_range = "off"

    setpoint = 276.6
    endpoint = 474.9
    temperatureController.setpoint = setpoint
    PID(setpoint)
    step = 10
    hold_time = 0

    while True:
        temperature = temperatureController.temperature_A

        with open(fileName, 'a', newline='') as csvfile:
            header = ["Timestamp", "Temperatures", "SetPoints"]
            writer = csv.DictWriter(csvfile, fieldnames=header)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(
                {
                    "Timestamp": second,
                    "Temperatures": temperature,
                    "SetPoints": setpoint
                }
            )
        second += 1
        time.sleep(1)

        if setpoint >= temperature - 0.1 and setpoint <= temperature + 0.1:
            hold_time += 1
            print("Hold time of {}K in second: {}".format(temperature, hold_time))
            if hold_time >= 60:
                # ohmcounter_front = 0
                # while ohmcounter_front < 10:
                #     now = dt.now().time()
                #     #RecordOhm(temperatureController.temperature_A, now) #Trigger Measurement Instruments
                #     ohmcounter_front += 1
                # StartProcess(MosfetIdVd, temperatureController.temperature_A)
                MosfetIdVd(temperatureController.temperature_A)
                MosfetIdVg(temperatureController.temperature_A)
                # Live Plot Id Vd
                StartProcess(LivePlotIdVd_IdVg)
                time.sleep(1)
                print("P: {}, I: {}, D: {}".format(temperatureController.gain, temperatureController.reset, temperatureController.rate))
                setpoint += step
                if setpoint > endpoint:
                    temperatureController.heater_range = "off"
                    print("Measurement Done.")
                    break
                temperatureController.setpoint = setpoint
                PID(setpoint)
                print("Changing to new setting point: {}".format(setpoint))
                
        else:
            hold_time = 0
            print("Hold time clear")

    csvfile.close()

def LivePlot():
    time.sleep(2)
    def animate(self):
        date = datetime.date.today()
        DIR = 'Data/temperature/{}'.format(date)
        fileNum = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        fileName = "Data/temperature/{}/temperature_{}.csv".format(date, fileNum)
        data = pd.read_csv(fileName)
        x_values = data['Timestamp']
        y_values = data['Temperatures']
        setpoint_values = data['SetPoints']
        plt.cla()
        
        if x_values[len(x_values)-1] > 60 and x_values[len(x_values)-1] < 3600 :
            plt.xlabel('Time(minutes)')
            plt.plot(x_values/60, y_values)
            plt.plot(x_values/60, setpoint_values)
            plt.plot(x_values/60, setpoint_values+0.1)
            plt.plot(x_values/60, setpoint_values-0.1)

        elif x_values[len(x_values)-1] > 3600 :
            plt.xlabel('Time(hours)')
            plt.plot(x_values/3600, y_values)
            plt.plot(x_values/3600, setpoint_values)
            plt.plot(x_values/3600, setpoint_values+0.1)
            plt.plot(x_values/3600, setpoint_values-0.1)
        else:
            plt.xlabel('Time(seconds)')
            plt.plot(x_values, y_values)
            plt.plot(x_values, setpoint_values)
            plt.plot(x_values, setpoint_values+0.1)
            plt.plot(x_values, setpoint_values-0.1)
        
        plt.ylabel('Temperatures(Kelvin)')
        plt.title('LakeShore330 Temperature Controller')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
    time.sleep(0.1)
    ani = FuncAnimation(plt.gcf(), animate, 1000)

    plt.tight_layout()
    plt.show()

def LivePlotIdVd_IdVg():
    # def animate(self):
    date = datetime.date.today()
    DIR_IdVd = 'Data/MOSFET_IdVd/{}'.format(date)
    fileNum_IdVd = len([name for name in os.listdir(DIR_IdVd) if os.path.isfile(os.path.join(DIR_IdVd, name))])
    fileName_IdVd = "Data/MOSFET_IdVd/{}/MOSFET_IdVd_{}.csv".format(date, fileNum_IdVd)

    DIR_IdVg = 'Data/MOSFET_IdVg/{}'.format(date)
    fileNum_IdVg = len([name for name in os.listdir(DIR_IdVg) if os.path.isfile(os.path.join(DIR_IdVg, name))])
    fileName_IdVg = "Data/MOSFET_IdVg/{}/MOSFET_IdVg_{}.csv".format(date, fileNum_IdVg)

    datas_IdVd = pd.read_csv(fileName_IdVd)
    datas_IdVg = pd.read_csv(fileName_IdVg)
    points_IdVd = 11
    points_IdVg = 30
    index_IdVd = 0
    index_IdVg = 0
    x_datas_IdVd = []
    y_datas_IdVd = []

    x_datas_IdVg = []
    y_datas_IdVg = []

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('MOSFET Characteristic')

    while index_IdVd <= len(datas_IdVd):
        x_datas_IdVd.append(datas_IdVd["Drain_Voltage"][index_IdVd:index_IdVd+points_IdVd])
        y_datas_IdVd.append(datas_IdVd["Drain_Current"][index_IdVd:index_IdVd+points_IdVd])
        index_IdVd += points_IdVd

    while index_IdVg <= len(datas_IdVg):
        x_datas_IdVg.append(datas_IdVg["Gate_Voltage"][index_IdVg:index_IdVg+points_IdVg])
        y_datas_IdVg.append(datas_IdVg["Drain_Current"][index_IdVg:index_IdVg+points_IdVg])
        index_IdVg += points_IdVg

    plt.cla()
    index_plot = 0
    while index_plot <= len(datas_IdVd)/points_IdVd-1:
        ax1.plot(x_datas_IdVd[index_plot], y_datas_IdVd[index_plot], label="Vg={}V".format(datas_IdVd["Gate_Voltage"][(points_IdVd)*index_plot]))
        ax1.legend(ncol=2)
        index_plot += 1

    index_plot = 0
    while index_plot <= len(datas_IdVg)/points_IdVg - 1:
        ax2.plot(x_datas_IdVg[index_plot], y_datas_IdVg[index_plot], label="Vd={}V".format(datas_IdVg["Drain_Voltage"][(points_IdVg)*index_plot]))
        ax2.legend(ncol=2)
        index_plot += 1

        # plt.xlabel("Drain Voltage Vd(V)")
        # plt.ylabel("Drain Current Id(A)")
    
    # ani = FuncAnimation(plt.gcf(), animate, 1000)

    plt.tight_layout()
    plt.show()

def StartProcess(Target):
    P = Process(target=Target)
    P.start()

def MosfetIdVd(temp):
    gate = Keithley2400("GPIB0::8")
    drain = Keithley2420("GPIB0::6")
    gate.source_voltage = 0
    drain.source_voltage = 0
    drain.compliance_current = 2
    gate.enable_source()
    gate.measure_current()
    drain.enable_source()
    drain.measure_current()
    drainvoltage_min = -0.5
    drainvoltage_max = 0.5
    gatevoltage = 0

    date = datetime.date.today()
    DIR = 'Data/MOSFET_IdVd/{}'.format(date)
    try:
        os.mkdir(DIR)
    except OSError:
        print ("Creation of the directory %s failed" % DIR)
    else:
        print ("Successfully created the directory %s " % DIR)
    # time.sleep(0.1)
    fileNum = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) + 1
    fileName = "Data/MOSFET_IdVd/{}/MOSFET_IdVd_{}.csv".format(date, fileNum)

    while gatevoltage <= 3:
        gate.source_voltage = gatevoltage
        while drainvoltage_min <= drainvoltage_max:
            drain.source_voltage = drainvoltage_min
            # fileName = "MOSFET_IdVd.csv"
            now = dt.now().time()
            with open(fileName, 'a', newline='') as csvfile:
                header = ["Timestamp", "Temperature", "Gate_Voltage", "Gate_Current","Drain_Voltage", "Drain_Current"]
                writer = csv.DictWriter(csvfile, fieldnames=header)
                if csvfile.tell() == 0:
                    writer.writeheader()
                writer.writerow(
                    {
                        "Timestamp": now,
                        "Temperature": temp,
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
        gatevoltage += 0.1
        print("Gate Voltage: ", gatevoltage)
        drainvoltage_min = -0.5 # Drain Voltage Reset Point
        time.sleep(1)

    gate.source_voltage = 0
    drain.source_voltage = 0
    gate.disable_source()
    drain.disable_source()

def MosfetIdVg(temp):
    gate = Keithley2400("GPIB0::8")
    drain = Keithley2420("GPIB0::6")
    gate.source_voltage = 0
    drain.source_voltage = 0
    drain.compliance_current = 2
    gate.enable_source()
    gate.measure_current()
    drain.enable_source()
    drain.measure_current()
    drainvoltage_min = 1.5
    drainvoltage_max = 2.5
    gatevoltage = 0

    date = datetime.date.today()
    DIR = 'Data/MOSFET_IdVg/{}'.format(date)
    try:
        os.mkdir(DIR)
    except OSError:
        print ("Creation of the directory %s failed" % DIR)
    else:
        print ("Successfully created the directory %s " % DIR)
    # time.sleep(0.1)
    fileNum = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) + 1
    fileName = "Data/MOSFET_IdVg/{}/MOSFET_IdVg_{}.csv".format(date, fileNum)

    while drainvoltage_min <= drainvoltage_max:
        drain.source_voltage = drainvoltage_min
        while gatevoltage <= 3 :
            gate.source_voltage = gatevoltage
            # fileName = "MOSFET_IdVd.csv"
            now = dt.now().time()
            with open(fileName, 'a', newline='') as csvfile:
                header = ["Timestamp", "Temperature", "Gate_Voltage", "Gate_Current","Drain_Voltage", "Drain_Current"]
                writer = csv.DictWriter(csvfile, fieldnames=header)
                if csvfile.tell() == 0:
                    writer.writeheader()
                writer.writerow(
                    {
                        "Timestamp": now,
                        "Temperature": temp,
                        "Gate_Voltage": gate.source_voltage,
                        "Gate_Current": gate.current,
                        "Drain_Voltage": drain.source_voltage,
                        "Drain_Current": drain.current
                    }
                )
            csvfile.close()
            time.sleep(1)
            gatevoltage += 0.1
            print("Drain Voltage: ", drainvoltage_min)
        drainvoltage_min += 0.1
        print("Gate Voltage: ", gatevoltage)
        gatevoltage = 0 # Gate Voltage Reset Point
        time.sleep(1)

    gate.source_voltage = 0
    drain.source_voltage = 0
    gate.disable_source()
    drain.disable_source()


def main():
    P1 = Process(target=TempLoop)
    P2 = Process(target=LivePlot)
    P1.start()
    P2.start()
    P1.join()
    P2.join()

if __name__ == "__main__":
    main()