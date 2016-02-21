import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
import SimulationWidget

app = QApplication(sys.argv)

class SimulationWidgetTest(unittest.TestCase):
    '''Test the SimulationWidget UI'''
    def setUp(self):
        '''Create the GUI'''
        self.widget = SimulationWidget.SimulationWidget()

    def test_default_controller_id(self):
        self.assertEqual(self.widget.controllerID_line.text(), "")

    def test_default_facility_id(self):
        self.assertEqual(self.widget.facility_line.text(), "")

    def test_default_workstation_id(self):
        self.assertEqual(self.widget.workstationID_line.text(), "")

    def test_default_role(self):
        self.assertEqual(self.widget.role_cmbox.currentText(),"Procedural Enroute")

    def test_default_responsibility(self):
        self.assertEqual(self.widget.responsibility_cmbox.currentText(), "Planning")

    def test_default_operational(self):
        self.assertEqual(self.widget.operational_cmbox.currentText(), "SC")

    def test_login_with_defaults(self):
        # Should not pass, because the controller, facility and workstations IDs are not set
        self.assertIsNone(self.widget.login())


suite = unittest.TestLoader().loadTestsFromTestCase(SimulationWidgetTest)
unittest.TextTestRunner(verbosity=2).run(suite)
        
