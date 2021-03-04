from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QFormLayout, QLabel,
QLineEdit, QGroupBox, QComboBox, QSpinBox, QWidget, QVBoxLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys

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
        self.instrumentsSettingBox()
        self.livePlot()
        self.mainLayout()
        self.show()

    def cintraLogo(self):
        self.logo = QLabel(self)
        pixmap = QPixmap("cintra.png")
        self.logo.setPixmap(pixmap)

    def instrumentsSettingBox(self):
        self.settingGroupBox = QGroupBox("Instruments Setting")
        layout = QFormLayout()
        layout.addRow(QLabel("Name:"), QLineEdit())
        layout.addRow(QLabel("Country:"), QComboBox())
        layout.addRow(QLabel("Age:"), QSpinBox())
        self.settingGroupBox.setLayout(layout)

    def livePlot(self):
        self.graph = pg.PlotWidget()
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]
        self.graph.setBackground('w')
        self.graph.setTitle("Your Title Here", color="b", size="30pt")
        styles = {"color": "#f00", "font-size": "20px"}
        self.graph.setLabel("left", "Temperature (°C)", **styles)
        self.graph.setLabel("bottom", "Hour (H)", **styles)
        self.graph.addLegend()
        self.graph.showGrid(x=True, y=True)
        self.graph.setXRange(0, 10, padding=0)
        self.graph.setYRange(20, 55, padding=0)
        pen = pg.mkPen(color=(255, 0, 0))
        self.graph.plot(hour, temperature, name="Sensor 1",  pen=pen, symbol='+', symbolSize=30, symbolBrush=('b'))

    def mainLayout(self):
        vBox = QVBoxLayout()
        vBox.addWidget(self.logo)
        vBox.addWidget(self.settingGroupBox)
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