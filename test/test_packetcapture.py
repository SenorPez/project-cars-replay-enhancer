"""
Tests packetcapture script.
"""
import sys
import unittest
from unittest.mock import patch, MagicMock, mock_open

from replayenhancer.packetcapture import main as packetcapture


class Testpacketcapture(unittest.TestCase):
    """
    Tests packetcapture script.
    """
    @unittest.skipIf(sys.version_info < (3, 5), "Not supported.")
    @patch('replayenhancer.packetcapture.os', autospec=True)
    @patch('replayenhancer.packetcapture.socket', autospec=True)
    def test(self, mock_socket, mock_os):
        mock_os.path.exists.return_value = False

        mock_data = MagicMock()

        mock_udp_socket = MagicMock()
        mock_udp_socket.recvfrom.return_value = (mock_data, None)

        mock_socket.socket.return_value = mock_udp_socket

        m = mock_open()
        with patch('replayenhancer.packetcapture.open', m) as mock_file_open:
            packetcapture(runonce=True)

            mock_socket.socket.assert_called_once_with(
                mock_socket.AF_INET,
                mock_socket.SOCK_DGRAM)
            mock_udp_socket.setsockopt.assert_called_once_with(
                mock_socket.SOL_SOCKET,
                mock_socket.SO_REUSEADDR,
                1)
            mock_udp_socket.bind.assert_called_once_with(("", 5606))

            exist_args, _ = mock_os.path.exists.call_args
            make_args, _ = mock_os.makedirs.call_args
            self.assertEqual('packetdata', exist_args[0].split('-')[0])
            self.assertEqual('packetdata', make_args[0].split('-')[0])

            mock_udp_socket.recvfrom.called_with(65565)

            args, kwargs = mock_file_open.call_args
            self.assertTrue('wb' in args)
            mock_file = m()
            mock_file.write.assert_called_once_with(mock_data)
            mock_file.close.assert_called_once_with()

            rm_args, _ = mock_os.rmdir.call_args
            self.assertEqual('packetdata', rm_args[0].split('-')[0])

    @unittest.skipIf(sys.version_info >= (3, 5), "Newer version available.")
    @patch('replayenhancer.packetcapture.os', autospec=True)
    @patch('replayenhancer.packetcapture.socket', autospec=True)
    def test_pre35(self, mock_socket, mock_os):
        mock_os.path.exists.return_value = False

        mock_data = MagicMock()

        mock_udp_socket = MagicMock()
        mock_udp_socket.recvfrom.return_value = (mock_data, None)

        mock_socket.socket.return_value = mock_udp_socket

        m = mock_open()
        with patch('builtins.open', m) as mock_file_open:
            packetcapture(runonce=True)

            mock_socket.socket.assert_called_once_with(
                mock_socket.AF_INET,
                mock_socket.SOCK_DGRAM)
            mock_udp_socket.setsockopt.assert_called_once_with(
                mock_socket.SOL_SOCKET,
                mock_socket.SO_REUSEADDR,
                1)
            mock_udp_socket.bind.assert_called_once_with(("", 5606))

            exist_args, _ = mock_os.path.exists.call_args
            make_args, _ = mock_os.makedirs.call_args
            self.assertEqual('packetdata', exist_args[0].split('-')[0])
            self.assertEqual('packetdata', make_args[0].split('-')[0])

            mock_udp_socket.recvfrom.called_with(65565)

            args, kwargs = mock_file_open.call_args
            self.assertTrue('wb' in args)
            mock_file = m()
            mock_file.write.assert_called_once_with(mock_data)
            mock_file.close.assert_called_once_with()

            rm_args, _ = mock_os.rmdir.call_args
            self.assertEqual('packetdata', rm_args[0].split('-')[0])

if __name__ == "__main__":
    unittest.main()
