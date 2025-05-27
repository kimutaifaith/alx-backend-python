#!/usr/bin/env python3
"""
Unit and integration tests for the client.GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import requests
import fixtures  # assuming this contains org_payload, repos_payload, expected_repos, apache2_repos
@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])

class TestGithubOrgClient(unittest.TestCase):
    """
    Unit test suite for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json", autospec=True)
    def test_org(self, org_name: str, mock_get_json) -> None:
        """
        Test that GithubOrgClient.org returns the correct value and calls
        get_json once with the expected URL.
        """
        mock_get_json.return_value = {"org": org_name}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, {"org": org_name})

    def test_public_repos_url(self) -> None:
        """
        Test that _public_repos_url returns the correct repos_url from the org.
        """
        fake_payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
        client = GithubOrgClient("test_org")

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value=fake_payload
        ):
            url = client._public_repos_url
            self.assertEqual(url, fake_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json) -> None:
        """
        Test that GithubOrgClient.public_repos returns expected list of repo names.
        """
        repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = repos_payload

        client = GithubOrgClient("test_org")

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/test_org/repos"
        ) as mock_public_repos_url:

            repos = client.public_repos
            expected_repos = [repo["name"] for repo in repos_payload]

            self.assertEqual(repos, expected_repos)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test_org/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected) -> None:
        """
        Test GithubOrgClient.has_license returns correct boolean based on
        repo license key matching the given license_key.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos using real payloads
    but mocking external HTTP calls only.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Setup patcher for requests.get and configure side_effect to return
        different payloads depending on the URL requested.
        """
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Side effect function to mock requests.get().json()
        def side_effect(url, *args, **kwargs):
            mock_resp = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_resp.json.return_value = cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = {}
            return mock_resp

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Stop patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Test the public_repos property returns the expected list of repo names
        using real fixtures and mocked HTTP requests.
        """
        client = GithubOrgClient("google")
        repos = client.public_repos
        self.assertEqual(repos, self.expected_repos)
        # Optionally, test the apache2 license filter if applicable
        apache2_repos = [
            repo for repo in repos
            if GithubOrgClient.has_license(
                next(r for r in self.repos_payload if r["name"] == repo),
                "apache-2.0"
            )
        ]
        self.assertEqual(apache2_repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
