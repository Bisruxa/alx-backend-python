#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock
from utils import get_json
# class TestAccessNestedMap(unittest.TestCase):  
#     @parameterized.expand([
#         ({"a": 1}, ("a",), 1),
#         ({"a": {"b": 2}}, ("a",), {"b": 2}),
#         ({"a": {"b": 2}}, ("a", "b"), 2),
#     ])
#     def test_access_nested_map(self, nested_map, path, expected):
#         self.assertEqual(access_nested_map(nested_map, path), expected)
#         @parameterized.expand([
#         ({}, ("a",), 1),
#         ({"a": 1}, ("a","b"), {"b": 2}),
#     ])
#     def test_access_nested_map_exception(self):
#         with self.assertRaises(KeyError) as context:
#             access_nested_map(nested_map, path)
#             self.assertEqual(str(context.exception), expected_error)
class TestGetJson(unittest.TestCase):

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for test_url, test_payload in test_cases:
            # Configure the mock to return a response with the expected JSON payload
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            # Call the function
            result = get_json(test_url)

            # Assertions
            self.assertEqual(result, test_payload)
            mock_get.assert_called_once_with(test_url)

            # Reset mock for the next iteration
            mock_get.reset_mock()

if __name__ == "__main__":
    unittest.main()
