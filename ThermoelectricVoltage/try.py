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

LivePlotIdVd_IdVg()