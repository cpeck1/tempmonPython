# append the project bin to the sys search path
import sys
sys.path.append("../bin/models")
sys.path.append("./bin/models")

import unittest
from unittest.mock import MagicMock
from datetime import datetime
from alarm_specification import AlarmSpecification

class AlarmSpecificationTest(unittest.TestCase):
    def setUp(self):
        self.alarm_spec = AlarmSpecification()
    
    def tearDown(self):
        self.alarm_spec = None

class DefaultUninitializedStateTest(AlarmSpecificationTest):
    pass

class AccessorTest(AlarmSpecificationTest):
    pass

class AddRuleTest(AlarmSpecificationTest):
    pass

class SatisfiedByTest(AlarmSpecificationTest):
    pass
