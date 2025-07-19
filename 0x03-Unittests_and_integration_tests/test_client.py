#!/usr/bin/env python3

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, MagicMock, PropertyMock
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

class TestGithubOrgClient(unittest.TestCase):
  @parameterized.expand([
    ("goggle",),
    ("abc",),
  ])
  @patch('client.get_json')
  def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns expected payload."""
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org  # Access the @property

        self.assertEqual(result, expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload
        
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"
            client = GithubOrgClient("testorg")
            repos = client.public_repos()
            
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")


  @parameterized.expand([
    ({"license": {"key": "my_license"}}, "my_license", True),
    ({"license": {"key": "other_license"}}, "my_license", True)
  ])
  def test_has_license(self,repo,license_key,expected):
    result = GithubOrgClient.has_license(repo, license_key)
    self.assertEqual(result, expected)
  def test_public_repos_url(self):
        """Test _public_repos_url property."""
        client = GithubOrgClient("testorg")

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value={"repos_url": "https://api.github.com/orgs/testorg/repos"}
        ) as mock_org:
            result = client._public_repos_url
            self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")
            mock_org.assert_called_once()

@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and return values based on URLs"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Setup mock behavior: requests.get(url).json()
        def side_effect(url):
            mock_resp = MagicMock()
            if url == f"https://api.github.com/orgs/testorg":
                mock_resp.json.return_value = cls.org_payload
            elif url == f"https://api.github.com/orgs/testorg/repos":
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo names"""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters repos by license correctly"""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
 


