import os
import re


class UniqueFileNameEnumerator:
    """This is used on the satelite and ground stations
    so that the ground station knows what the filename of the next file on the satelite is"""

    def __init__(self, file_dir):
        self._dir = file_dir

        if not os.path.exists(self._dir):
            os.makedirs(self._dir)

        self._current_file_name = self._get_starting_file()

    def _get_starting_file(self):
        i = 0

        files = os.listdir(self._dir)
        for file in files:
            file_num = self._get_file_num(file)
            if file_num > i:
                i = file_num
        i += 1

        return self._get_file_name(i)

    def move_to_next_file(self):
        file_num = self._get_file_num(self._current_file_name)
        file_num += 1
        self._current_file_name = self._get_file_name(file_num)

    def _get_file_name(self, num):
        return os.path.join(self._dir, "file%s.txt" % num)

    @staticmethod
    def _get_file_num(file):
        if file is None:
            return 0

        cleaned = re.sub("[^0-9]", "", file)
        if cleaned == '':
            return 0

        return int(cleaned)

    def get_current_file_name(self):
        return self._current_file_name
