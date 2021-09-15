"""Test health check endpoint"""
import unittest
from flask_testing import TestCase
from . import TestAbstractClass

class TestHealth(TestAbstractClass, TestCase):
    """Test case for health check endpoint"""

    def test(self) -> None:
        """Tests health check endpoint

        Checks that health check endpoint returns 200 and JSON
        body {'status': 'ok'}

        Raise:
            AssertionError: If status code is not 200 or JSON
                            body does not match

        """
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'ok'})

if __name__ == "__main__":
    unittest.main()
