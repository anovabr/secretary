import os
import stat
import tempfile
import unittest

from secretary.envfile import set_values


class SetValuesTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, ".env")
        with open(self.path, "w") as fh:
            fh.write("IG_ACCOUNTS=a,b\nIG_A_TOKEN=old-a\n\n# note\nIG_B_TOKEN=old-b\nOTHER=x=y\n")
        os.chmod(self.path, 0o644)

    def tearDown(self):
        self.dir.cleanup()

    def read(self):
        with open(self.path) as fh:
            return fh.read()

    def test_replaces_only_the_named_key(self):
        set_values(self.path, {"IG_A_TOKEN": "new-a"})
        self.assertEqual(self.read(), "IG_ACCOUNTS=a,b\nIG_A_TOKEN=new-a\n\n# note\nIG_B_TOKEN=old-b\nOTHER=x=y\n")

    def test_appends_a_missing_key(self):
        set_values(self.path, {"NEW": "1"})
        self.assertTrue(self.read().endswith("OTHER=x=y\nNEW=1\n"))

    def test_file_ends_private(self):
        set_values(self.path, {"IG_B_TOKEN": "new-b"})
        self.assertEqual(stat.S_IMODE(os.stat(self.path).st_mode), 0o600)

    def test_leaves_no_temp_files(self):
        set_values(self.path, {"IG_B_TOKEN": "new-b"})
        self.assertEqual(os.listdir(self.dir.name), [".env"])


if __name__ == "__main__":
    unittest.main()
