"""Tests swagger endpoint"""
import unittest
from flask_testing import TestCase
from . import TestAbstractClass

class TestSwagger(TestAbstractClass, TestCase):
    """Test case for swagger endpoint"""

    def test(self):
        """Tests swagger endpoint

        Checks that swagger endpoint returns 308

        Raise:
            AssertionError: If status code is not 308

        """
        response = self.client.get('/swagger')
        self.assertEqual(response.status_code, 308)

if __name__ == "__main__":
    unittest.main()
