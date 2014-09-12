# append the project bin to the sys search path
import sys
sys.path.append("../bin/models")
sys.path.append("./bin/models")

import unittest
from unittest.mock import MagicMock
from datetime import datetime
import time
from context import Context

class UserTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

class DefaultUninitializedStateTest(UserTest):
    pass

class AccessorTest(UserTest):
    pass
