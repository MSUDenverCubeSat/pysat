import unittest
import os
import shutil
from pysat.Logger import Logger


class LoggerTests(unittest.TestCase):

    temp_dir = "/home/pi/Temp_Files"
    final_dir = "/home/pi/Done_Files"

    def setUp(self):
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass

        try:
            shutil.rmtree(self.final_dir)
        except:
            pass

    def test_run_logger(self):
        logger = Logger(self.temp_dir, self.final_dir)

        for num in range(1, logger._lines_per_file + 2):
            logger.log("Line %s" % num)

        file1 = open(os.path.join(self.final_dir, "file1.txt"), "r")
        lines = file1.readlines()
        file1.close()
        self.assertEqual(lines.__len__(), logger._lines_per_file)
        num = 1
        for line in lines:
            self.assertEqual(line, "Line %s\n" % num)
            num += 1

        file2 = open(os.path.join(self.temp_dir, "file2.txt"), "r")
        lines = file2.readlines()
        file2.close()
        self.assertEqual(lines.__len__(), 1)
        self.assertEqual(lines[0], "Line %s\n" % num)

        self.setUp()

    def test_run_logger_moves_old_files(self):
        logger = Logger(self.temp_dir, self.final_dir)
        logger.log("Line 1")
        self.assertEqual(os.path.exists(os.path.join(self.temp_dir, "file1.txt")), True)

        for num in range(2, logger._lines_per_file + 1):
            logger.log("Line %s" % num)

        self.assertEqual(os.path.exists(os.path.join(self.temp_dir, "file1.txt")), True)
        self.assertEqual(os.path.exists(os.path.join(self.final_dir, "file1.txt")), False)

        logger.log("Line 1")
        self.assertEqual(os.path.exists(os.path.join(self.temp_dir, "file1.txt")), False)
        self.assertEqual(os.path.exists(os.path.join(self.temp_dir, "file2.txt")), True)
        self.assertEqual(os.path.exists(os.path.join(self.final_dir, "file1.txt")), True)

        self.setUp()

    def test_run_logger_picks_up_where_left_off(self):
        logger = Logger(self.temp_dir, self.final_dir)
        logger.log(1)

        logger = Logger(self.temp_dir, self.final_dir)
        logger.log(2)

        file1 = open(os.path.join(self.final_dir, "file1.txt"), "r")
        lines = file1.readlines()
        file1.close()
        self.assertEqual(lines.__len__(), 1)
        self.assertEqual(lines[0], "1\n")

        file2 = open(os.path.join(self.temp_dir, "file2.txt"), "r")
        lines = file2.readlines()
        file2.close()
        self.assertEqual(lines.__len__(), 1)
        self.assertEqual(lines[0], "2\n")

        self.setUp()
