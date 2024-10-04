import unittest
import tempfile
import os
import ast
from static_analyser import StaticAnalyser, PatternIdentifier

class TestStaticAnalyser(unittest.TestCase):
    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False)
        self.test_filename = self.test_file.name
        
    def tearDown(self):
        os.unlink(self.test_filename)
        
    def analyse_code(self, code):
        with open(self.test_filename, 'w') as f:
            f.write(code)
        analyser = StaticAnalyser(self.test_filename)
        analyser.analyse(PatternIdentifier())
        return analyser.report
    
    def test_print_in_try_block(self):
        code = """
try:
    print("This is a print statement inside try block")
except:
    pass
"""
        report = self.analyse_code(code)
        self.assertEqual(len(report), 1)
        self.assertIn("Print statement found in try block", report[0]['explanation'])

    def test_logging_in_try_block(self):
        code = """
import logging
try:
    logging.info("This is a log entry inside try block")
except:
    pass
"""
        report = self.analyse_code(code)
        self.assertEqual(len(report), 1)
        self.assertIn("Logging statement found in try block", report[0]['explanation'])
    
    def test_no_print_or_logging_in_try_block(self):
        code = """
try:
    num = 0
    num += 1
except:
    print("Error occurred")
"""
        report = self.analyse_code(code)
        self.assertEqual(len(report), 0)
        
    def test_print_outside_try_block(self):
        code = """
print("Printing outside try block")
try:
    num = 0
    num += 1
except:
    pass
"""
        report = self.analyse_code(code)
        self.assertEqual(len(report), 0)

    def test_multiple_prints_logs(self):
        code = """
try:
    print("This is first print in try block")
    logging.info("This is a log message")
    print("Second print in try block")
except:
    print("First print in except block")
finally:
    print("First print in finally block")
"""
        report = self.analyse_code(code)
        self.assertEqual(len(report), 3)
