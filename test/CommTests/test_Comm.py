import unittest
from unittest.mock import patch, call
import asyncio
from pysat.Comm import Comm


class CommTests(unittest.TestCase):

    baudrate = 57600
    device = "/dev/ttyUSB0"

    @patch('builtins.print')
    def test_run_list_directory(self, mock_print):
        loop = asyncio.get_event_loop()
        comm = Comm(loop, self.device, self.baudrate)

        loop.run_until_complete(self.run_list_directory(comm))

        self.assertEqual(mock_print.mock_calls, [
            call('Waiting for mavsdk_server to be ready...'),
            call('Connected to mavsdk_server!'),
            call('List remote directory for', '/home:'),
            call('List directory failed')
        ])

    async def run_list_directory(self, comm):
        result = await comm.list_directory("/home")
        self.assertEqual(result.success, False)

    @patch('builtins.print')
    def test_run_clean_directory_list(self, mock_print):
        loop = asyncio.get_event_loop()
        comm = Comm(loop, self.device, self.baudrate)

        self.assertEqual(mock_print.mock_calls, [
            call('Waiting for mavsdk_server to be ready...'),
            call('Connected to mavsdk_server!')
        ])

        remote_dirs = ['', 'S', 'files', 'files', 'tmp']
        result = comm._clean_directory_list("/home", remote_dirs)
        self.assertEqual(result, ['/home/files', '/home/tmp'])

    @patch('builtins.print')
    def test_run_download_file(self, mock_print):
        loop = asyncio.get_event_loop()
        comm = Comm(loop, self.device, self.baudrate)

        loop.run_until_complete(self.run_download_file(comm))

        self.assertEqual(mock_print.mock_calls, [
            call('Waiting for mavsdk_server to be ready...'),
            call('Connected to mavsdk_server!'),
            call('Downloading remote file', '/home/files/file1.txt', 'to local directory', '/home/files'),
            call('Download file failed')
        ])

    async def run_download_file(self, comm):
        result = await comm.download_file("/home/files/file1.txt", "/home/files")
        self.assertEqual(result.success, False)

    @patch('builtins.print')
    def test_run_are_files_identical(self, mock_print):
        loop = asyncio.get_event_loop()
        comm = Comm(loop, self.device, self.baudrate)

        loop.run_until_complete(self.run_are_files_identical(comm))

        self.assertEqual(mock_print.mock_calls, [
            call('Waiting for mavsdk_server to be ready...'),
            call('Connected to mavsdk_server!'),
            call('Checking if files are identical failed')
        ])

    async def run_are_files_identical(self, comm):
        result = await comm.are_files_identical("/home/files/file1.txt", "/home/files/file1.txt")
        self.assertEqual(result.success, False)

    @patch('builtins.print')
    def test_run_delete_remote_file(self, mock_print):
        loop = asyncio.get_event_loop()
        comm = Comm(loop, self.device, self.baudrate)

        loop.run_until_complete(self.run_delete_remote_file(comm))

        self.assertEqual(mock_print.mock_calls, [
            call('Waiting for mavsdk_server to be ready...'),
            call('Connected to mavsdk_server!'),
            call('Deleting remote file', '/home/files/file1.txt'),
            call('Deleting file failed')
        ])

    async def run_delete_remote_file(self, comm):
        result = await comm.delete_remote_file("/home/files/file1.txt")
        self.assertEqual(result.success, False)
