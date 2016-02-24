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
        self.widget = SimulationWidget.SimulationWidget(testMode = True)

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
        self.assertFalse(self.widget.login())
        self.assertFalse(self.widget.isLogged())

    def test_login_normal(self):
        self.widget.setLogged(False)
        self.widget.controllerID_line.setText("420")
        self.widget.facility_line.setText("420")
        self.widget.workstationID_line.setText("420")

        self.assertTrue(self.widget.login())
        self.assertTrue(self.widget.isLogged())

    def test_login_when_already_logged_in(self):
        self.widget.setLogged(True)
        self.widget.controllerID_line.setText("420")
        self.widget.facility_line.setText("420")
        self.widget.workstationID_line.setText("420")

        self.assertFalse(self.widget.login())
        self.assertTrue(self.widget.isLogged())

        # test for a button click
    def test_login_button_press(self):
        self.widget.setLogged(False)
        self.widget.controllerID_line.setText("420")
        self.widget.facility_line.setText("420")
        self.widget.workstationID_line.setText("420")

        QTest.mouseClick(self.widget.login_btn, Qt.LeftButton)
        self.assertTrue(self.widget.isLogged())

    def test_logout_with_defaults(self):
        self.assertFalse(self.widget.login())
        self.assertFalse(self.widget.isLogged())

    def test_logout_normal(self):
        self.widget.setLogged(True)
        self.widget.controllerID_line.setText("420")
        self.widget.facility_line.setText("420")
        self.widget.workstationID_line.setText("420")

        self.assertTrue(self.widget.logout())
        self.assertFalse(self.widget.isLogged())

    def test_logout_when_not_logged_in(self):
        self.widget.setLogged(False)
        self.widget.controllerID_line.setText("420")
        self.widget.facility_line.setText("420")
        self.widget.workstationID_line.setText("420")

        self.assertFalse(self.widget.logout())
        self.assertFalse(self.widget.isLogged())


    def test_role_change_normal(self):
        self.widget.setLogged(True)
        self.widget.controllerID_line.setText("420")
        self.widget.facility_line.setText("420")
        self.widget.workstationID_line.setText("420")

        self.assertTrue(self.widget.rolechange())
        self.assertTrue(self.widget.isLogged())

# This code will actually execute the tests
suite = unittest.TestLoader().loadTestsFromTestCase(SimulationWidgetTest)
unittest.TextTestRunner(verbosity=2).run(suite)
        
