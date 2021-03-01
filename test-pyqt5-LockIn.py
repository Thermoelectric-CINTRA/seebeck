import sys
from PyQt5.QtWidgets import (QDialog, QApplication, QPushButton, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt

from pymeasure.instruments.nf import LI5660
from pymeasure.instruments.hp import HP34401A

class MyWidget(QDialog):
    def __init__(self):
        super().__init__()

        # initialize instrument
        self.init_instruments()

        self.button = QPushButton("Click me!")
        self.text = QLabel("Hello User")
        self.text.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.startBuffer)
        self.show()

    # initialize measurement instrument
    def init_instruments(self):
        # contruct instruments and pass the address
        self.lockin = LI5660("GPIB0::1")
        self.ammeter = HP34401A("GPIB0::2")
        
        self.lockin.coupling('AC')
        self.lockin.grounding('Ground')
        self.lockin.input_terminal('AB')
        self.lockin.reference_signal('Internal')
        self.lockin.clear_all_buffer()
        self.lockin.data_feed('Buffer1',  30)
        self.lockin.data_feed_control('Buffer1', 'Always')
        self.lockin.data_points('Buffer1', 16)
        self.lockin.source_trigger("Bus")
        self.lockin.delay(0)
        
    # start buffer and record data from NF Lock-In 
    def startBuffer(self):
        # 
        print(self.lockin.check_errors())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.resize(300, 200)
    sys.exit(app.exec_())