"""Test advice endpoint"""
from datetime import datetime
import unittest
from flask_testing import TestCase
from . import TestAbstractClass

mock_data = {
    "content": "string",
    "description": "string",
    "domain": "string",
    "end_time": datetime.now().isoformat(),
    "facebook": True,
    "goal": 0,
    "instagram": True,
    "max_set_price": 0,
    "min_set_price": 0,
    "set_count": 0,
    "start_time": datetime.now().isoformat(),
    "title": "string",
    "type": "string",
    "website": True,
    "youtube": True
}

class TestAdvice(TestAbstractClass, TestCase):
    """Test case for advice endpoint"""

    param_type = {
        'score': float
    }

    def test(self) -> None:
        """Tests advice endpoint

        Checks that advice endpoint returns 200 and correct
        JSON body

        Raise:
            AssertionError: If status code is not 200 or JSON
                            body does not match

        """
        response = self.client.post('/advice', json=mock_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        for k, v in self.param_type.items():
            self.assertIn(k, response.json)
            self.assertIsInstance(response.json[k], v)

    def test_get(self) -> None:
        """Tests 405 response with get request

        Checks that advice endpoint returns 405 for get request

        Raise:
            AssertionError: If status code is not 405

        """
        response = self.client.get('/advice', json=mock_data)
        print(response.json)
        self.assertEqual(response.status_code, 405)

    def test_empty(self) -> None:
        """Tests 422 response with empty input

        Checks that advice endpoint returns 422 for empty input

        Raise:
            AssertionError: If status code is not 422

        """
        response = self.client.post('/advice')
        print(response.json)
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()
