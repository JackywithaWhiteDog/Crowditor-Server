"""Test project list endpoint"""
import unittest
from flask_testing import TestCase
from . import TestAbstractClass

class TestProjectList(TestAbstractClass, TestCase):
    """Test case for project list endpoint"""

    param_type = {
        'projects': list
    }

    def test(self) -> None:
        """Tests project list endpoint

        Checks that project list endpoint returns 200 and correct
        JSON body

        Raise:
            AssertionError: If status code is not 200 or JSON
                            body does not match

        """
        response = self.client.get('/projects')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        for k, v in self.param_type.items():
            self.assertIn(k, response.json)
            self.assertIsInstance(response.json[k], v)

if __name__ == "__main__":
    unittest.main()
