from pysat.Automatons.BaseAutomaton import BaseAutomaton
from pysat.Logger import Logger
from enum import Enum
import os


class FtpAutomaton (BaseAutomaton):

    def __init__(self, comm, loop, remote_dir, local_dir):
        self.interval_sec = 5
        self.comm = comm
        self.loop = loop
        self.remote_dir = remote_dir
        self.local_dir = local_dir
        self.logger = Logger(local_dir, local_dir)
        self.file_state = FileState.NeedDownload

    def execute(self):
        self.loop.run_until_complete(self.reconcileFiles())

    async def reconcileFiles(self):
        remote_file = os.path.join(self.remote_dir, os.path.basename(self.logger.current_file_name))
        local_file = self.logger.current_file_name

        if self.file_state == FileState.NeedDownload:
            downloaded_result = await self.comm.downloadFile(remote_file, self.local_dir)
            if downloaded_result.success:
                if downloaded_result.result:
                    print("Download worked: ", downloaded_result.result)
                    self.file_state = FileState.NeedIdenticalCheck

        if self.file_state == FileState.NeedIdenticalCheck:
            if os.path.exists(local_file):
                isSame_result = await self.comm.areFilesIdentical(local_file, remote_file)
                if isSame_result.success:
                    if not isSame_result.result:
                        print("Local file and remote file are not the same. Retrying download.")
                        os.remove(local_file)
                        self.file_state = FileState.NeedDownload
                    else:
                        print("Local file and remote file are the same.")
                        self.file_state = FileState.NeedDelete
            else:
                print("Local file does not exist. Retrying download")
                self.file_state = FileState.NeedDownload

        if self.file_state == FileState.NeedDelete:
            delete_result = await self.comm.deleteRemoteFile(remote_file)
            if delete_result.success:
                if delete_result.result:
                    print("Remote file deleted.")
                    self.logger.current_file_name = self.logger.get_next_file(self.logger.current_file_name)
                    self.file_state = FileState.NeedDownload


class FileState(Enum):
    NeedDownload = 1
    NeedIdenticalCheck = 2
    NeedDelete = 3
