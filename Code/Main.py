import sys
from PyQt4.QtGui import *
from SimulationWidget import SimulationWidget

# Create an PyQT4 application object.
a = QApplication(sys.argv)

# The QWidget widget is the base class of all user interface objects in PyQt4.
w = SimulationWidget()

# Set window title  
w.setWindowTitle("CALS SIM")

# Show window
w.show()

sys.exit(a.exec_())