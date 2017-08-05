import sys
sys.path.insert(0, "..")

import unittest
from easy_install import atomic_easy_file

class TestAtomicEasyFile(unittest.TestCase):
    def test_simple(self):
        stdout_n = sys.stdout
        sys.stdout = open("tmp1_output.txt", "w")
        atomic_easy_file("test1.yml")
        sys.stdout.close()
        sys.stdout = stdout_n

        contents = []
        for line in open("tmp1_output.txt", "r"):
            contents.append(line.strip())

        self.assertEqual(len(contents), 1)
        self.assertEqual(contents[0], "YAML file to install nvm.")
        # self.assertEqual(contents[1], "Hello world")

if __name__ == "__main__":
    unittest.main()
