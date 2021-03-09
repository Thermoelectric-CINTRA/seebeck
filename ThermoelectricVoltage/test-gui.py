from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QFormLayout, QLabel,
QLineEdit, QGroupBox, QComboBox, QSpinBox, QWidget, QVBoxLayout, QDialogButtonBox)
from PyQt5.QtGui import QPixmap, QDoubleValidator
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys

from pymeasure.instruments.keithley import Keithley2420
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments.lakeshore import LakeShore330

import csv
import os, os.path
import datetime
from datetime import datetime as dt
import time
from multiprocessing import Process
from matplotlib.animation import FuncAnimation
import pandas as pd
import matplotlib.pyplot as plt

class TemperatureLoop(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, tempStart, tempEnd, tempStep, parent=None):
        super().__init__()
        self.TempStart = tempStart
        self.TempEnd = tempEnd
        self.TempStep = tempStep

    def tempLoop(self):
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

        setpoint = self.TempStart
        endpoint = self.TempEnd
        temperatureController.setpoint = setpoint
        PID(setpoint)
        step = self.TempStep
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
                    # MosfetIdVd(temperatureController.temperature_A)
                    # MosfetIdVg(temperatureController.temperature_A)
                    # StartProcess(LivePlotIdVd_IdVg)
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

class TemperaturePlot(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__()

    def livePlot(self):
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()
        
    def initializeUI(self):
        """Initialize the window and display its contents."""
        self.setMinimumSize(1200, 600)
        self.setWindowTitle("CINTRA - Thermoelectric Characteristic Measurement")

        """Initialize the window layout."""
        self.cintraLogo()
        self.temperatureLoopSettingBox()
        self.idvdSettingBox()
        self.idvgSettingBox()
        self.runTest()
        self.ividPlot()
        self.mainLayout()
        self.show()

    def cintraLogo(self):
        self.logo = QLabel(self)
        pixmap = QPixmap("cintra.png")
        self.logo.setPixmap(pixmap)

    def temperatureLoopSettingBox(self):
        self.temperatureGroupBox = QGroupBox("Temperature Loop Setting")
        layout = QFormLayout()
        self.tempStart = QLineEdit()
        self.tempEnd = QLineEdit()
        self.tempStep = QLineEdit()
        self.tempStart.setValidator(QDoubleValidator(0.99, 999.99, 2))
        self.tempEnd.setValidator(QDoubleValidator(0.99, 999.99, 2))
        self.tempStep.setValidator(QDoubleValidator(0.99, 999.99, 2))
        layout.addRow(QLabel("Temperature Start:"), self.tempStart)
        layout.addRow(QLabel("Temperature End:"), self.tempEnd)
        layout.addRow(QLabel("Temperature Step:"), self.tempStep)
        self.temperatureGroupBox.setLayout(layout)

    def idvdSettingBox(self):
        self.idvdGroupBox = QGroupBox("Id-Vd Setting")
        layout = QFormLayout()
        self.idvdGateVoltageStart = QLineEdit()
        self.idvdGateVoltageEnd = QLineEdit()
        self.idvdDrainVoltageStart = QLineEdit()
        self.idvdDrainVoltageEnd = QLineEdit()
        self.idvdGateVoltageStart.setValidator(QDoubleValidator(0.99, 99.99, 2))
        self.idvdGateVoltageEnd.setValidator(QDoubleValidator(0.99, 99.99, 2))
        self.idvdDrainVoltageStart.setValidator(QDoubleValidator(0.99, 99.99, 2))
        self.idvdDrainVoltageEnd.setValidator(QDoubleValidator(0.99, 99.99, 2))
        layout.addRow(QLabel("Gate Voltage (Start Point):"), self.idvdGateVoltageStart)
        layout.addRow(QLabel("Gate Voltage (End Point):"), self.idvdGateVoltageEnd)
        layout.addRow(QLabel("Drain Voltage (Start Point):"), self.idvdDrainVoltageStart)
        layout.addRow(QLabel("Drain Voltage (End Point):"), self.idvdDrainVoltageEnd)
        self.idvdGroupBox.setLayout(layout)

    def idvgSettingBox(self):
        self.idvgGroupBox = QGroupBox("Id-Vg Setting")
        layout = QFormLayout()
        self.idvgGateVoltageStart = QLineEdit()
        self.idvgGateVoltageEnd = QLineEdit()
        self.idvgDrainVoltageStart = QLineEdit()
        self.idvgDrainVoltageEnd = QLineEdit()
        self.idvgGateVoltageStart.setValidator(QDoubleValidator(0.99, 99.99, 2))
        self.idvgGateVoltageEnd.setValidator(QDoubleValidator(0.99, 99.99, 2))
        self.idvgDrainVoltageStart.setValidator(QDoubleValidator(0.99, 99.99, 2))
        self.idvgDrainVoltageEnd.setValidator(QDoubleValidator(0.99, 99.99, 2))
        layout.addRow(QLabel("Drain Voltage (Start Point):"), self.idvgDrainVoltageStart)
        layout.addRow(QLabel("Drain Voltage (End Point):"), self.idvgDrainVoltageEnd)
        layout.addRow(QLabel("Gate Voltage (Start Point):"), self.idvgGateVoltageStart)
        layout.addRow(QLabel("Gate Voltage (End Point):"), self.idvgGateVoltageEnd)
        self.idvgGroupBox.setLayout(layout)

    def runTest(self):
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.button(QDialogButtonBox.Ok).setText("Start")
        self.buttonBox.accepted.connect(self.triggerInstruments)
        self.buttonBox.rejected.connect(self.abortInstruments)

    def triggerInstruments(self):
        print("Gate voltage start at: ", self.idvdGateVoltageStart.text())
        print("Gate voltage end at: ", self.idvdGateVoltageEnd.text())
        print("Drain voltage start at: ", self.idvdDrainVoltageStart.text())
        print("Drain voltage end at: ", self.idvdDrainVoltageEnd.text())
        # self.initInstrument()
        # self.StartProcess(self.tempLoop, float(self.tempStart.text()), float(self.tempEnd.text()))
        # self.tempLoop(float(self.tempStart.text()), float(self.tempEnd.text()))
        self.thread = QThread()
        # self.thread_2 = QThread()
        self.TempLoop = TemperatureLoop(
            float(self.tempStart.text()),
            float(self.tempEnd.text()), 
            float(self.tempStep.text())
        )
        self.TempLoop.moveToThread(self.thread)

        self.tempPlot = TemperaturePlot()
        self.tempPlot.moveToThread(self.thread)

        self.thread.started.connect(self.TempLoop.tempLoop)
        self.thread.started.connect(self.tempPlot.livePlot)

        self.thread.start()
    def abortInstruments(self):
        pass

    def StartProcess(self, Target, start, end):
        P = Process(target=Target, args=(start, end))
        P.start()

    def initInstrument(self):
        gate = Keithley2400("GPIB0::8")
        gate.measure_current()

    def ividPlot(self):
        self.graph = pg.PlotWidget()
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]
        self.graph.setBackground('w')
        self.graph.setTitle("IV Characteristic", color="b", size="30pt")
        styles = {"color": "#f00", "font-size": "20px"}
        self.graph.setLabel("left", "Drain Current (A)", **styles)
        self.graph.setLabel("bottom", "Gate Voltage (V)", **styles)
        self.graph.addLegend()
        self.graph.showGrid(x=True, y=True)
        self.graph.setXRange(0, 10, padding=0)
        self.graph.setYRange(20, 55, padding=0)
        pen = pg.mkPen(color=(255, 0, 0))
        self.graph.plot(hour, temperature, name="Drain Current",  pen=pen, symbol='+', symbolSize=30, symbolBrush=('b'))

    def mainLayout(self):
        vBox = QVBoxLayout()
        vBox.addWidget(self.logo)
        vBox.addWidget(self.temperatureGroupBox)
        vBox.addWidget(self.idvdGroupBox)
        vBox.addWidget(self.idvgGroupBox)
        vBox.addWidget(self.buttonBox)
        vBox.setAlignment(Qt.AlignTop)
        hBox = QHBoxLayout()
        hBox.addLayout(vBox)
        hBox.addWidget(self.graph)
        mainFrame = QWidget()
        self.setCentralWidget(mainFrame)
        mainFrame.setLayout(hBox)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())