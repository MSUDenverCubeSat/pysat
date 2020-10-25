import os
import os.path
import re
import shutil

class Logger:

    def __init__(self):
        self._lines_per_file = 3
        self._lines_written = 0
        self._temp_dir = "/home/pi/Temp_Files"
        self._final_dir = "/home/pi/Done_Files"

        if not os.path.exists(self._temp_dir):
            os.makedirs(self._temp_dir)

        if not os.path.exists(self._final_dir):
            os.makedirs(self._final_dir)

        self._current_file_name = self._get_starting_file()

    def _get_starting_file(self):
        i = 1

        files = os.listdir(self._temp_dir)
        for file in files:
            file_num = self._get_file_num(file)
            if file_num > i:
                i = file_num
        if i > 1:
            i += 1

        return os.path.join(self._temp_dir, "file%s.txt" % i)

    def get_next_file(self, current_file):
        file_num = self._get_file_num(current_file)
        file_num += 1
        return os.path.join(self._temp_dir, "file%s.txt" % file_num)

    def _get_file_num(self, file):
        return int(re.sub("[^0-9]", "", file))
    
    def log(self, input):
        line = str(input)

        if self._lines_written < self._lines_per_file:
            self._write_line(line)
        else:
            self._lines_written = 0
            self._current_file_name = self.get_next_file(self._current_file_name)
            self._write_line(line)
            self._move_old_files_to_dest_path()

    def _write_line(self, line):
        file = ""
        try:
            file = open(self._current_file_name, "a+")
            file.write(line + "\r")
            self._lines_written += 1
        except Exception as e:
            print(e)
        finally:
            file.close()

    def _move_old_files_to_dest_path(self):
        files = os.listdir(self._temp_dir)
        for file in files:
            if file != os.path.basename(self._current_file_name):
                shutil.move(os.path.join(self._temp_dir, file), os.path.join(self._final_dir, file))
