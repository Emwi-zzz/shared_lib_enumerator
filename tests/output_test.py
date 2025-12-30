import unittest
import subprocess
import os
import tempfile
import shutil

import shared_lib_enumerator as sle

class TestLibInspector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Compile a real .so library for testing."""
        cls.work_dir = tempfile.mkdtemp()
        cls.lib_path = os.path.join(cls.work_dir, "libtest.so")
        src_path = os.path.join(cls.work_dir, "test.c")

        # C source with various visibility/types
        c_code = """
        void a_func() {}       // Public
        void _hidden_func() {}     // Filtered by sive_
        void z_func() {}       // Public (test sorting)
        static void static_func() {} // Not exported
        """
        with open(src_path, "w") as f:
            f.write(c_code)

        try:
            subprocess.run(
                ["gcc", "-shared", "-fPIC", src_path, "-o", cls.lib_path],
                check=True, capture_output=True
            )
        except Exception as e:
            shutil.rmtree(cls.work_dir)
            raise RuntimeError(f"GCC compilation failed: {e}")

    @classmethod
    def tearDownClass(cls):
        """Cleanup temporary files."""
        shutil.rmtree(cls.work_dir)

    def setUp(self):
        self.inspector = sle

    def test_functional_inspection(self):
        """Verify extraction and alphabetical sorting of public symbols."""
        results = self.inspector.inspect(self.lib_path, sive_=True)
        expected = ["a_func", "z_func"]
        self.assertEqual(results, expected)

    def test_sive_filter_off(self):
        """Verify that underscores are included when sive_ is False."""
        results = self.inspector.inspect(self.lib_path, sive_=False)
        self.assertIn("_hidden_func", results)

    def test_invalid_path(self):
        """Ensure subprocess error is raised for missing files."""
        with self.assertRaises(subprocess.CalledProcessError):
            self.inspector.inspect("/tmp/non_existent_lib.so")

if __name__ == "__main__":
    unittest.main()