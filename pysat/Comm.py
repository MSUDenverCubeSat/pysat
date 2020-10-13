from mavsdk import System
import time, os

class Comm:

    def __init__(self, loop, device, baudrate):
        self._loop = loop

        self._drone = System(mavsdk_server_address='localhost', port=50051)
        # self.drone = System()
        self._loop.run_until_complete(self._drone.connect(system_address="serial://" + device + ":" + str(baudrate)))

    async def listDirectory(self, dir):
        print("List remote directory for ", dir, ":")
        done = False
        files = []
        while not done:
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
                time.sleep(1)
        return self.cleanDirectoryList(dir, files)

    def cleanDirectoryList(self, dir, files):
        ret = []
        for file in files:
            if file != 'S':
                cleanFile = os.path.join(dir, os.path.basename(file.split('\t')[0]))

                if not ret.__contains__(cleanFile):
                    ret.append(cleanFile)
        return ret

    async def downloadFile(self, remoteFile, localDir):
        print("Downloading remote file ", remoteFile, " to local directory ", localDir)
        done = False
        while not done:
            try:
                progress = self._drone.ftp.download(remoteFile, localDir)
                async for byteDisplay in progress:
                    print("Bytes downloaded: ", byteDisplay.bytes_transferred, "/", byteDisplay.total_bytes)
                done = True
            except:
                localFile = os.path.join(localDir, os.path.basename(remoteFile))
                if os.path.exists(localFile):
                    os.remove(localFile)
                try:
                    await self._drone.ftp.reset()
                except:
                    pass
                print("Download file failed... trying again")
                time.sleep(1)
        return done

    async def areFilesIdentical(self, localFile, remoteFile):
        done = False
        isSame = False
        while not done:
            try:
                isSame = await self._drone.ftp.are_files_identical(localFile, remoteFile)
                done = True
            except:
                try:
                    await self._drone.ftp.reset()
                except:
                    pass
                print("Checking if files are identical failed... trying again")
                time.sleep(1)
        return isSame

    async def deleteRemoteFile(self, remoteFile):
        print("Deleting remote file ", remoteFile)
        done = False
        deleted = False
        while not done:
            try:
                await self._drone.ftp.remove_file(remoteFile)
                deleted = True
                done = True
            except:
                try:
                    await self._drone.ftp.reset()
                except:
                    pass
                print("Deleting file failed... trying again")
                time.sleep(1)
        return deleted
