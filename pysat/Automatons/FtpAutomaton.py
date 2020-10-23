from pysat.Automatons.BaseAutomaton import BaseAutomaton
import os

class FtpAutomaton (BaseAutomaton):

    def __init__(self, comm, loop, remote_dir, local_dir):
        self.interval_sec = 5
        self.comm = comm
        self.loop = loop
        self.remote_dir = remote_dir
        self.local_dir = local_dir

    def execute(self):
        self.loop.run_until_complete(self.reconcileFiles())

    async def reconcileFiles(self):

        result = await self.comm.listDirectory(self.remote_dir)
        files = result.result

        for file in files:
            done = False
            while not done:
                downloaded = await self.comm.downloadFile(file, self.local_dir)
                print("Download worked: ", downloaded)

                localFile = os.path.join(self.local_dir, os.path.basename(file))
                if os.path.exists(localFile):
                    isSame = await self.comm.areFilesIdentical(localFile, file)
                    if not isSame:
                        print("Local file and remote file are not the same. Retrying download.")
                        os.remove(localFile)
                    else:
                        await self.comm.deleteRemoteFile(file)
                        done = True
                else:
                    print("Local file does not exist. Retrying download")
