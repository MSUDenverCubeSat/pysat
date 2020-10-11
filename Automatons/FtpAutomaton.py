from Automatons.BaseAutomaton import BaseAutomaton
import os
import time

class FtpAutomaton (BaseAutomaton):

    def __init__(self, drone, loop, remoteDir, localDir):
        self.interval_sec = 5
        self.drone = drone
        self.loop = loop
        self.remoteDir = remoteDir
        self.localDir = localDir

    def execute(self):
        self.loop.run_until_complete(self.reconcileFiles())

    async def reconcileFiles(self):

        #await self.drone.ftp.set_root_directory(self.remoteDir)

        files = await self.listDirectory(self.remoteDir)

        for file in files:
            done = False
            while not done:
                downloaded = await self.downloadFile(file, self.localDir)
                print("Download worked: ", downloaded)

                localFile = os.path.join(self.localDir, os.path.basename(file))
                if os.path.exists(localFile):
                    isSame = await self.areFilesIdentical(localFile, file)
                    if not isSame:
                        print("Local file and remote file are not the same. Retrying download.")
                        os.remove(localFile)
                    else:
                        await self.deleteRemoteFile(file)
                        done = True
                else:
                    print("Local file does not exist. Retrying download")

    async def listDirectory(self, dir):
        print("List remote directory for ", dir, ":")
        done = False
        files = []
        while not done:
            try:
                files = await self.drone.ftp.list_directory(dir)
                print(files)
                done = True
            except:
                try:
                    await self.drone.ftp.reset()
                except:
                    pass
                print("List directory failed... trying again")
                time.sleep(2)
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
                progress = self.drone.ftp.download(remoteFile, localDir)
                async for byteDisplay in progress:
                    print("Bytes downloaded: ", byteDisplay.bytes_transferred, "/", byteDisplay.total_bytes)
                done = True
            except:
                localFile = os.path.join(localDir, os.path.basename(remoteFile))
                if os.path.exists(localFile):
                    os.remove(localFile)
                try:
                    await self.drone.ftp.reset()
                except:
                    pass
                print("Download file failed... trying again")
                time.sleep(2)
        return done

    async def areFilesIdentical(self, localFile, remoteFile):
        done = False
        isSame = False
        while not done:
            try:
                isSame = await self.drone.ftp.are_files_identical(localFile, remoteFile)
                done = True
            except:
                try:
                    await self.drone.ftp.reset()
                except:
                    pass
                print("Checking if files are identical failed... trying again")
                time.sleep(2)
        return isSame

    async def deleteRemoteFile(self, remoteFile):
        print("Deleting remote file ", remoteFile)
        done = False
        deleted = False
        while not done:
            try:
                await self.drone.ftp.remove_file(remoteFile)
                deleted = True
                done = True
            except:
                try:
                    await self.drone.ftp.reset()
                except:
                    pass
                print("Deleting file failed... trying again")
                time.sleep(2)
        return deleted
