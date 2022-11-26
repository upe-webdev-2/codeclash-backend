import os
import sys
import unittest

import coverage

def run():
    os.environ['IS_DEBUG'] = 'TRUE'

    cov = coverage.Coverage(branch = True)
    cov.start()

    tests = unittest.TestLoader().discover('.')
    ok = unittest.TextTestRunner(verbosity = 2).run(tests).wasSuccessful()

    cov.stop()
    print('')
    cov.report(omit = ["tests/*", "venv*/*", "setup.py"])

    sys.exit(0 if ok else 1)