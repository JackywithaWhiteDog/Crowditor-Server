"""Test advice endpoint"""
import unittest
from flask_testing import TestCase
from . import TestAbstractClass

class TestAdvice(TestAbstractClass, TestCase):
    """Test case for advice endpoint"""

    param = ['keywords', 'success_rate', 'goal', 'duration_days', 'description_length', 'content_length']

    def test(self) -> None:
        """Tests advice endpoint

        Checks that advice endpoint returns 200 and correct
        JSON body

        Raise:
            AssertionError: If status code is not 200 or JSON
                            body does not match

        """
        response = self.client.get('/advice')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIn('data', response.json)
        for v in response.json['data'].values():
            for p in self.param:
                self.assertIn(p, v)

if __name__ == "__main__":
    unittest.main()
