"""Tests 404 Response"""
import unittest
from flask_testing import TestCase
from . import TestAbstractClass

class Test404(TestAbstractClass, TestCase):
    """Test case for 404 resoponse"""

    def test(self) -> None:
        """Tests 404 response

        Requests a non-existent resource and check
        the status code to be 404

        Raise:
            AssertionError: If status code is not 404

        """
        response = self.client.get('/404')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
