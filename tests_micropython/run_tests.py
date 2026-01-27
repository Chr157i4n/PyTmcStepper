import os
import sys
import unittest

# wichtig: damit machine.py gefunden wird
sys.path.insert(0, "tests")

loader = unittest.TestLoader()
suite = unittest.TestSuite()

for fname in os.listdir("tests"):
    if fname.startswith("test_") and fname.endswith(".py"):
        modname = fname[:-3]
        module = __import__(modname)
        suite.addTests(loader.loadTestsFromModule(module))

runner = unittest.TextTestRunner()
result = runner.run(suite)

# Exit-Code für GitHub Actions
if not result.wasSuccessful():
    sys.exit(1)
