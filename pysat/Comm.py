from mavsdk import System
import os
from pysat.Result import Result


class Comm:
    """Handles all of the communication over the radios
    https://github.com/mavlink/MAVSDK-Python
    http://mavsdk-python-docs.s3-website.eu-central-1.amazonaws.com/index.html"""

    def __init__(self, loop, server_address, server_port, device, baudrate):
        self._loop = loop
        self._drone = System(mavsdk_server_address=server_address, port=server_port)
        self._loop.run_until_complete(self._drone.connect(system_address="serial://" + device + ":" + str(baudrate)))

    async def list_directory(self, remote_dir):
        print("List remote directory for", remote_dir + ":")
        worked = False
        files = []
        try:
            files = await self._drone.ftp.list_directory(remote_dir)
            print(files)
            worked = True
        except:
            try:
                await self._drone.ftp.reset()
            except:
                pass
            print("List directory failed")
        return Result(worked, self._clean_directory_list(remote_dir, files))

    def _clean_directory_list(self, directory, files):
        ret = []
        for file in files:
            if file != 'S' and file != '':     # for some reason the list directory will occasionally return 'S'
                clean_file = os.path.join(directory, os.path.basename(file.split('\t')[0]))

                if not ret.__contains__(clean_file):
                    ret.append(clean_file)
        return ret

    async def download_file(self, remote_file, local_dir):
        print("Downloading remote file", remote_file, "to local directory", local_dir)
        worked = False
        try:
            progress = self._drone.ftp.download(remote_file, local_dir)
            async for byteDisplay in progress:
                print("Bytes downloaded: ", byteDisplay.bytes_transferred, "/", byteDisplay.total_bytes)
            worked = True
        except:
            local_file = os.path.join(local_dir, os.path.basename(remote_file))
            if os.path.exists(local_file):
                os.remove(local_file)
            try:
                await self._drone.ftp.reset()
            except:
                pass
            print("Download file failed")
        return Result(worked, worked)

    async def are_files_identical(self, local_file, remote_file):
        done = False
        is_same = False
        try:
            is_same = await self._drone.ftp.are_files_identical(local_file, remote_file)
            done = True
        except:
            try:
                await self._drone.ftp.reset()
            except:
                pass
            print("Checking if files are identical failed")
        return Result(done, is_same)

    async def delete_remote_file(self, remote_file):
        print("Deleting remote file", remote_file)
        done = False
        deleted = False
        try:
            await self._drone.ftp.remove_file(remote_file)
            deleted = True
            done = True
        except:
            try:
                await self._drone.ftp.reset()
            except:
                pass
            print("Deleting file failed")
        return Result(done, deleted)
