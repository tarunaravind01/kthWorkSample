import unittest
from subprocess import run, PIPE

class AppTestCase(unittest.TestCase):
    def test_app_runs_without_errors(self):
        # Test case to ensure the app runs without any errors
        result = run(['python3', 'cliApp.py', 'instance1'], stdout=PIPE, stderr=PIPE, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("instance1", result.stdout)
        self.assertIn("Configuration completed successfully", result.stdout)

    def test_app_handles_invalid_instance_name(self):
        # Test case to ensure the app handles invalid instance name gracefully
        result = run(['python3', 'cliApp.py', 'invalid_instance'], stdout=PIPE, stderr=PIPE, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Could not match supplied host pattern", result.stderr)

if __name__ == '__main__':
    unittest.main()
