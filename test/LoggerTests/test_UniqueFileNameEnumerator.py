import unittest
import os
import shutil
from pysat.UniqueFileNameEnumerator import UniqueFileNameEnumerator


class UniqueFileNameEnumeratorTest(unittest.TestCase):

    directory = '/home/pi/Temp_Files'

    def setUp(self):
        try:
            shutil.rmtree(self.directory)
        except:
            pass

    def test_enumerating_from_scratch(self):
        self.assertEqual(os.path.exists(self.directory), False)

        enumerator = UniqueFileNameEnumerator(self.directory)
        self.assertEqual(os.path.exists(self.directory), True)
        self.assertEqual(enumerator.get_current_file_name(), os.path.join(self.directory, "file1.txt"))

        for num in range(2, 500):
            enumerator.move_to_next_file()
            self.assertEqual(enumerator.get_current_file_name(), os.path.join(self.directory, "file%s.txt" % num))

        self.setUp()

    def test_enumerating_pickup_from_left_off(self):
        enumerator = UniqueFileNameEnumerator(self.directory)
        self.assertEqual(enumerator.get_current_file_name(), os.path.join(self.directory, "file1.txt"))

        file = open(os.path.join(self.directory, "file100.txt"), "w")
        file.write("This is a test.")
        file.close()

        enumerator = UniqueFileNameEnumerator(self.directory)
        self.assertEqual(enumerator.get_current_file_name(), os.path.join(self.directory, "file101.txt"))

        self.setUp()
