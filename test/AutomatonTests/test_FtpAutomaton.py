import unittest
from unittest.mock import patch, call
import asyncio
import os
import shutil
import time
from pysat.Comm import Comm
from pysat.Automatons.FtpAutomaton import FtpAutomaton, FileState


class FtpAutomatonTests(unittest.TestCase):

    baudrate = 57600
    device = "/dev/ttyUSB0"
    remote_dir = "/home/pi/Done_Files"
    local_dir = "/home/pi/files"

    def setUp(self):
        try:
            shutil.rmtree(self.local_dir)
        except:
            pass

    @patch('builtins.print')
    def test_run_execute_twice(self, mock_print):

        loop = asyncio.get_event_loop()
        comm = Comm(loop, self.device, self.baudrate)
        ftp = FtpAutomaton(comm, loop, self.remote_dir, self.local_dir)
        self.assertEqual(ftp.__active__, False)
        ftp.start()
        self.assertEqual(ftp.__active__, True)

        time.sleep(ftp.interval_sec * ftp.calls_per_execute * 3)
        self.assertEqual(ftp.__active__, True)
        ftp.stop()
        self.assertEqual(ftp.__active__, False)

        time.sleep(ftp.interval_sec * ftp.calls_per_execute * 3)
        self.assertEqual(ftp.__active__, False)

        self.assertEqual(mock_print.mock_calls, [
            call('Waiting for mavsdk_server to be ready...'),
            call('Connected to mavsdk_server!'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again')
        ])

        self.setUp()

    @patch('builtins.print')
    def test_run_start_stop(self, mock_print):

        loop = asyncio.get_event_loop()
        comm = Comm(loop, self.device, self.baudrate)
        ftp = FtpAutomaton(comm, loop, self.remote_dir, self.local_dir)
        self.assertEqual(ftp.__active__, False)
        ftp.start()
        self.assertEqual(ftp.__active__, True)

        time.sleep(ftp.interval_sec + 1)
        self.assertEqual(ftp.__active__, True)
        ftp.stop()
        self.assertEqual(ftp.__active__, False)

        time.sleep(ftp.interval_sec * ftp.calls_per_execute * 3)
        self.assertEqual(ftp.__active__, False)

        self.assertEqual(mock_print.mock_calls, [
            call('Waiting for mavsdk_server to be ready...'),
            call('Connected to mavsdk_server!'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again')
        ])

        self.setUp()

    @patch('builtins.print')
    def test_run_execute(self, mock_print):
        loop = asyncio.get_event_loop()
        comm = Comm(loop, self.device, self.baudrate)
        ftp = FtpAutomaton(comm, loop, self.remote_dir, self.local_dir)
        ftp.execute()

        self.assertEqual(mock_print.mock_calls, [
            call('Waiting for mavsdk_server to be ready...'),
            call('Connected to mavsdk_server!'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again')
        ])

        self.assertEqual(ftp.file_state == FileState.NeedDownload, True)

    @patch('builtins.print')
    def test_run_download_file(self, mock_print):
        loop = asyncio.get_event_loop()
        comm = Comm(loop, self.device, self.baudrate)
        ftp = FtpAutomaton(comm, loop, self.remote_dir, self.local_dir)

        loop.run_until_complete(self.download_file(ftp))

        self.assertEqual(mock_print.mock_calls, [
            call('Waiting for mavsdk_server to be ready...'),
            call('Connected to mavsdk_server!'),
            call('Downloading remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name())),
                 'to local directory', self.local_dir),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again'),
            call('Download file failed... trying again')
        ])

        self.setUp()

    async def download_file(self, ftp):
        await ftp._download_file()
        self.assertEqual(ftp.file_state == FileState.NeedDownload, True)

    @patch('builtins.print')
    def test_run_check_files_identical_file_does_not_exist(self, mock_print):
        loop = asyncio.get_event_loop()
        comm = Comm(loop, self.device, self.baudrate)
        ftp = FtpAutomaton(comm, loop, self.remote_dir, self.local_dir)
        ftp.file_state = FileState.NeedIdenticalCheck

        loop.run_until_complete(self.check_files_identical(ftp))

        self.assertEqual(mock_print.mock_calls, [
            call('Waiting for mavsdk_server to be ready...'),
            call('Connected to mavsdk_server!'),
            call('Local file does not exist. Retrying download')
        ])

        self.assertEqual(ftp.file_state == FileState.NeedDownload, True)

        self.setUp()

    @patch('builtins.print')
    def test_run_check_files_identical(self, mock_print):
        loop = asyncio.get_event_loop()
        comm = Comm(loop, self.device, self.baudrate)
        ftp = FtpAutomaton(comm, loop, self.remote_dir, self.local_dir)
        ftp.file_state = FileState.NeedIdenticalCheck

        file = open(ftp.file_enumerator.get_current_file_name(), 'w')
        file.write("Test")
        file.close()

        loop.run_until_complete(self.check_files_identical(ftp))

        self.assertEqual(mock_print.mock_calls, [
            call('Waiting for mavsdk_server to be ready...'),
            call('Connected to mavsdk_server!'),
            call('Checking if files are identical failed... trying again'),
            call('Checking if files are identical failed... trying again'),
            call('Checking if files are identical failed... trying again'),
            call('Checking if files are identical failed... trying again')
        ])

        self.assertEqual(ftp.file_state == FileState.NeedIdenticalCheck, True)

        self.setUp()

    async def check_files_identical(self, ftp):
        await ftp._check_files_identical()

    @patch('builtins.print')
    def test_run_delete_remote_file(self, mock_print):
        loop = asyncio.get_event_loop()
        comm = Comm(loop, self.device, self.baudrate)
        ftp = FtpAutomaton(comm, loop, self.remote_dir, self.local_dir)
        ftp.file_state = FileState.NeedDelete

        loop.run_until_complete(self.delete_remote_file(ftp))

        self.assertEqual(mock_print.mock_calls, [
            call('Waiting for mavsdk_server to be ready...'),
            call('Connected to mavsdk_server!'),
            call('Deleting remote file',
                 os.path.join(self.remote_dir, os.path.basename(ftp.file_enumerator.get_current_file_name()))),
            call('Deleting file failed... trying again'),
            call('Deleting file failed... trying again'),
            call('Deleting file failed... trying again'),
            call('Deleting file failed... trying again')
        ])

        self.assertEqual(ftp.file_state == FileState.NeedDelete, True)

        self.setUp()

    async def delete_remote_file(self, ftp):
        await ftp._delete_remote_file()
