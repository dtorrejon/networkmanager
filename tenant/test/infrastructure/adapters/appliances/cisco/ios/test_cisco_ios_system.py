import unittest
from unittest.mock import Mock, patch
from tenant.infraestructure.adapters.appliances.cisco.ios.cisco_ios_system import CiscoIosSystem
from tenant.domain.schemas.appliances.system.hostname import Hostname
from tenant.domain.schemas.appliances.system.restart import Restart


class TestCiscoIosSystem(unittest.TestCase):

    @patch('netmiko.BaseConnection')
    def test_successful_restart(self, MockBaseConnection):
        mock_connection = MockBaseConnection()
        mock_connection.send_command.return_value = "Proceed with reload? [confirm]"
        mock_connection.password = "password"
        system = CiscoIosSystem(mock_connection)
        system.connect.send_command.side_effect = "0x2102"
        result = system.restart()
        self.assertIsInstance(result, Restart)
        self.assertEqual(result.status, "nok")

    @patch('netmiko.BaseConnection')
    def test_unsuccessful_restart_due_to_configuration_register(self, MockBaseConnection):
        mock_connection = MockBaseConnection()
        mock_connection.send_command.return_value = "0x2101"
        mock_connection.password = "password"
        system = CiscoIosSystem(mock_connection)
        result = system.restart()
        self.assertIsInstance(result, Restart)
        self.assertEqual(result.status, "nok")

    @patch('netmiko.BaseConnection')
    def test_successful_hostname_change(self, MockBaseConnection):
        mock_connection = MockBaseConnection()
        mock_connection.send_command.return_value = "New hostname test, successfully updated"
        mock_connection.password = "password"
        system = CiscoIosSystem(mock_connection)
        result = system.set_hostname("test")
        assert isinstance(result, Hostname)
        self.assertEqual(result.status, "OK")

    @patch('netmiko.BaseConnection')
    def test_unsuccessful_hostname_change(self, MockBaseConnection):
        mock_connection = MockBaseConnection()
        mock_connection.send_command.return_value = "Failed to update hostname"
        mock_connection.password = "password"
        system = CiscoIosSystem(mock_connection)
        result = system.set_hostname("test")
        self.assertIsInstance(result, Hostname)
        self.assertEqual(result.status, "KO")


if __name__ == '__main__':
    unittest.main()
