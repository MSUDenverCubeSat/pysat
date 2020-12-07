from pysat.Automatons.BaseAutomaton import BaseAutomaton
from pysat.UniqueFileNameEnumerator import UniqueFileNameEnumerator
from enum import Enum
import os


class FtpAutomaton (BaseAutomaton):

    def __init__(self, comm, loop, remote_dir, local_dir):
        self._interval_sec = 2
        self._calls_per_execute = 5
        self._max_delete_retries = self._calls_per_execute
        self._current_delete_retry = 0
        self._comm = comm
        self._loop = loop
        self._remote_dir = remote_dir
        self._local_dir = local_dir
        self._file_enumerator = UniqueFileNameEnumerator(local_dir)
        self._file_state = FileState.NeedDownload
        self._file_actions = {FileState.NeedDownload: self._download_file,
                              FileState.NeedIdenticalCheck: self._check_files_identical,
                              FileState.NeedDelete: self._delete_remote_file}

    def execute(self):
        self._loop.run_until_complete(self._reconcile_files())

    async def _reconcile_files(self):
        for i in range(1, self._calls_per_execute + 1):
            await self._file_actions[self._file_state]()

    async def _download_file(self):
        remote_file = os.path.join(self._remote_dir, os.path.basename(self._file_enumerator.get_current_file_name()))
        downloaded_result = await self._comm.download_file(remote_file, self._local_dir)
        if downloaded_result.success:
            if downloaded_result.result:
                self._file_state = FileState.NeedIdenticalCheck

    async def _check_files_identical(self):
        if os.path.exists(self._file_enumerator.get_current_file_name()):
            remote_file = os.path.join(self._remote_dir,
                                       os.path.basename(self._file_enumerator.get_current_file_name()))
            is_same_result = await self._comm.are_files_identical(self._file_enumerator.get_current_file_name(),
                                                                  remote_file)
            if is_same_result.success:
                if not is_same_result.result:
                    print("Local file and remote file are not the same. Retrying download.")
                    os.remove(self._file_enumerator.get_current_file_name())
                    self._file_state = FileState.NeedDownload
                else:
                    print("Local file and remote file are the same.")
                    self._file_state = FileState.NeedDelete
        else:
            print("Local file does not exist. Retrying download")
            self._file_state = FileState.NeedDownload

    async def _delete_remote_file(self):
        remote_file = os.path.join(self._remote_dir, os.path.basename(self._file_enumerator.get_current_file_name()))
        delete_result = await self._comm.delete_remote_file(remote_file)
        if (delete_result.success and delete_result.result) or self._current_delete_retry >= self._max_delete_retries:
            print("Remote file deleted.")
            self._file_enumerator.move_to_next_file()
            self._file_state = FileState.NeedDownload
            self._current_delete_retry = 0
        else:
            self._current_delete_retry += 1


class FileState(Enum):
    NeedDownload = 1
    NeedIdenticalCheck = 2
    NeedDelete = 3
