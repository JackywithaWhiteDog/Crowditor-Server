"""Tests swagger UI"""
import unittest
from flask_testing import TestCase
from . import TestAbstractClass

class TestSwaggerUI(TestAbstractClass, TestCase):
    """Test case for swagger UI"""

    def test(self):
        """Tests swagger UI

        Checks that swagger UI returns 308

        Raise:
            AssertionError: If status code is not 308

        """
        response = self.client.get('/swagger-ui')
        self.assertEqual(response.status_code, 308)

if __name__ == "__main__":
    unittest.main()
