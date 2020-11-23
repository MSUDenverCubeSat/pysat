from pysat.Automatons.BaseAutomaton import BaseAutomaton
from pysat.UniqueFileNameEnumerator import UniqueFileNameEnumerator
from enum import Enum
import os


class FtpAutomaton (BaseAutomaton):

    def __init__(self, comm, loop, remote_dir, local_dir):
        self.interval_sec = 2
        self.calls_per_execute = 5
        self.comm = comm
        self.loop = loop
        self.remote_dir = remote_dir
        self.local_dir = local_dir
        self.file_enumerator = UniqueFileNameEnumerator(local_dir)
        self.file_state = FileState.NeedDownload
        self.file_actions = {FileState.NeedDownload: self._download_file,
                             FileState.NeedIdenticalCheck: self._check_files_identical,
                             FileState.NeedDelete: self._delete_remote_file}

    def execute(self):
        self.loop.run_until_complete(self._reconcileFiles())

    async def _reconcileFiles(self):
        for i in range(1, self.calls_per_execute + 1):
            await self.file_actions[self.file_state]()

    async def _download_file(self):
        remote_file = os.path.join(self.remote_dir, os.path.basename(self.file_enumerator.get_current_file_name()))
        downloaded_result = await self.comm.downloadFile(remote_file, self.local_dir)
        if downloaded_result.success:
            if downloaded_result.result:
                print("Download worked: ", downloaded_result.result)
                self.file_state = FileState.NeedIdenticalCheck

    async def _check_files_identical(self):
        if os.path.exists(self.file_enumerator.get_current_file_name()):
            remote_file = os.path.join(self.remote_dir, os.path.basename(self.file_enumerator.get_current_file_name()))
            is_same_result = await self.comm.areFilesIdentical(self.file_enumerator.get_current_file_name(), remote_file)
            if is_same_result.success:
                if not is_same_result.result:
                    print("Local file and remote file are not the same. Retrying download.")
                    os.remove(self.file_enumerator.get_current_file_name())
                    self.file_state = FileState.NeedDownload
                else:
                    print("Local file and remote file are the same.")
                    self.file_state = FileState.NeedDelete
        else:
            print("Local file does not exist. Retrying download")
            self.file_state = FileState.NeedDownload

    async def _delete_remote_file(self):
        remote_file = os.path.join(self.remote_dir, os.path.basename(self.file_enumerator.get_current_file_name()))
        delete_result = await self.comm.deleteRemoteFile(remote_file)
        if delete_result.success:
            if delete_result.result:
                print("Remote file deleted.")
                self.file_enumerator.move_to_next_file()
                self.file_state = FileState.NeedDownload


class FileState(Enum):
    NeedDownload = 1
    NeedIdenticalCheck = 2
    NeedDelete = 3
