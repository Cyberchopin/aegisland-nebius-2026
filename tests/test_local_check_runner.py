import socket
import unittest
from unittest.mock import patch
from run_local_checks import offline_connection


class OfflineConnectionTests(unittest.TestCase):
    def test_external_and_named_loopback_destinations_blocked_before_connect(self):
        with patch("run_local_checks._create_connection") as connect:
            for host in ("api.tokenfactory.nebius.com", "example.com", "localhost", "127.0.0.2"):
                with self.subTest(host=host), self.assertRaises(RuntimeError):
                    offline_connection((host, 443), timeout=5)
            connect.assert_not_called()

    def test_exact_loopback_connection_passes_through(self):
        with patch("run_local_checks._create_connection") as connect:
            offline_connection(("127.0.0.1", 12345), timeout=5)
            connect.assert_called_once_with(("127.0.0.1", 12345), timeout=5)
