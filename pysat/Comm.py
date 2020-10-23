from mavsdk import System
import time, os
from pysat.Result import Result

class Comm:

    def __init__(self, loop, device, baudrate):
        self._loop = loop

        self._drone = System(mavsdk_server_address='localhost', port=50051)
        # self.drone = System()
        self._loop.run_until_complete(self._drone.connect(system_address="serial://" + device + ":" + str(baudrate)))
        self._sleep_secs = 1
        self._retries = 10

    async def listDirectory(self, dir):
        print("List remote directory for ", dir, ":")
        done = False
        files = []
        num_try = 1
        while not done and num_try < self._retries:
            try:
                files = await self._drone.ftp.list_directory(dir)
                print(files)
                done = True
            except:
                try:
                    await self._drone.ftp.reset()
                except:
                    pass
                print("List directory failed... trying again")
                time.sleep(self._sleep_secs)
                num_try += 1
        return Result(done, self._cleanDirectoryList(dir, files))

    def _cleanDirectoryList(self, dir, files):
        ret = []
        for file in files:
            if file != 'S':     # for some reason the list directory will occasionally return 'S'
                cleanFile = os.path.join(dir, os.path.basename(file.split('\t')[0]))

                if not ret.__contains__(cleanFile):
                    ret.append(cleanFile)
        return ret

    async def downloadFile(self, remote_file, local_dir):
        print("Downloading remote file ", remote_file, " to local directory ", local_dir)
        done = False
        num_try = 1
        while not done and num_try < self._retries:
            try:
                progress = self._drone.ftp.download(remote_file, local_dir)
                async for byteDisplay in progress:
                    print("Bytes downloaded: ", byteDisplay.bytes_transferred, "/", byteDisplay.total_bytes)
                done = True
            except:
                localFile = os.path.join(local_dir, os.path.basename(remote_file))
                if os.path.exists(localFile):
                    os.remove(localFile)
                try:
                    await self._drone.ftp.reset()
                except:
                    pass
                print("Download file failed... trying again")
                time.sleep(self._sleep_secs)
                num_try += 1
        return Result(done, done)

    async def areFilesIdentical(self, local_file, remote_file):
        done = False
        isSame = False
        num_try = 1
        while not done and num_try < self._retries:
            try:
                isSame = await self._drone.ftp.are_files_identical(local_file, remote_file)
                done = True
            except:
                try:
                    await self._drone.ftp.reset()
                except:
                    pass
                print("Checking if files are identical failed... trying again")
                time.sleep(self._sleep_secs)
                num_try += 1
        return Result(done, isSame)

    async def deleteRemoteFile(self, remote_file):
        print("Deleting remote file ", remote_file)
        done = False
        deleted = False
        num_try = 1
        while not done and num_try < self._retries:
            try:
                await self._drone.ftp.remove_file(remote_file)
                deleted = True
                done = True
            except:
                try:
                    await self._drone.ftp.reset()
                except:
                    pass
                print("Deleting file failed... trying again")
                time.sleep(self._sleep_secs)
                num_try += 1
        return Result(done, deleted)
