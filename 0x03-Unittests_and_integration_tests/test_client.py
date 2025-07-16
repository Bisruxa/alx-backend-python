import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient
class TestGithubOrgClient(unittest.TestCase):
  @parameterized.expand([
    ("goggle",),
    ("abc",),
  ])
  @patch('client.get_json')
  def test_org(self, org_name, mock_get_json):
    expected = {"login": org_name}
    mock_get_json.return_value = expected

    client = GithubOrgClient(org_name)
    result = client.org  # Access property, not method

    self.assertEqual(result, expected)
    mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
