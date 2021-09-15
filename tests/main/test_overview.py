"""Test overview endpoint"""
import unittest
from flask_testing import TestCase
from . import TestAbstractClass

class TestOverview(TestAbstractClass, TestCase):
    """Test case for overview endpoint"""

    param = ['keywords', 'helpful_tokens', 'success_rate', 'achievement_rate', 'funds', 'domain_cnt', 'domain_success_rate', 'funds_ranking', 'achievement_rate_ranking']

    def test(self) -> None:
        """Tests overview endpoint

        Checks that overview endpoint returns 200 and correct
        JSON body

        Raise:
            AssertionError: If status code is not 200 or JSON
                            body does not match

        """
        response = self.client.get('/overview')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        for p in self.param:
            self.assertIn(p, response.json)

if __name__ == "__main__":
    unittest.main()
