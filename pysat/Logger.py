import os
import shutil
from pysat.UniqueFileNameEnumerator import UniqueFileNameEnumerator


class Logger:

    def __init__(self, temp_dir, final_dir):
        self._lines_per_file = 3
        self._lines_written = 0
        self._temp_dir = temp_dir
        self._final_dir = final_dir

        if not os.path.exists(self._temp_dir):
            os.makedirs(self._temp_dir)

        if not os.path.exists(self._final_dir):
            os.makedirs(self._final_dir)

        self.file_enumerator = UniqueFileNameEnumerator(self._temp_dir)
        self._move_old_files_to_dest_path()
    
    def log(self, line):
        line = str(line)

        if self._lines_written < self._lines_per_file:
            self._write_line(line)
        else:
            self._lines_written = 0
            self.file_enumerator.move_to_next_file()
            self._write_line(line)
            self._move_old_files_to_dest_path()

    def _write_line(self, line):
        file = ""
        try:
            file = open(self.file_enumerator.get_current_file_name(), "a+")
            file.write(line + "\r")
            self._lines_written += 1
        except Exception as e:
            print(e)
        finally:
            file.close()

    def _move_old_files_to_dest_path(self):
        files = os.listdir(self._temp_dir)
        for file in files:
            if file != os.path.basename(self.file_enumerator.get_current_file_name()):
                shutil.move(os.path.join(self._temp_dir, file), os.path.join(self._final_dir, file))
