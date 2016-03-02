import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from SimulationWidget import SimulationWidget

# Create an PyQT5 application object.
a = QApplication(sys.argv)

# The QWidget widget is the base class of all user interface objects in PyQt4.
w = SimulationWidget()

# Set window title  
w.setWindowTitle("CALS SIM")

# Show window
w.show()

sys.exit(a.exec_())