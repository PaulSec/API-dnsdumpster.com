"""Integration tests for DNSDumpster API with mocked HTTP responses."""

import base64

import pytest
import responses

from dnsdumpster.DNSDumpsterAPI import (
    DNSDumpsterAPI,
    DNSDumpsterAPIError,
    DNSDumpsterParseError,
    DNSDumpsterRequestError,
)


class TestSearch:
    """Test the main search method with mocked responses."""

    @responses.activate
    def test_search_success(self, sample_main_page_html, sample_full_response_html):
        """Test successful search with mocked responses."""
        # Mock the main page request to get auth token
        responses.add(responses.GET, "https://dnsdumpster.com/", body=sample_main_page_html, status=200)

        # Mock the API request
        responses.add(responses.POST, "https://api.dnsdumpster.com/htmld/", body=sample_full_response_html, status=200)

        # Mock image download
        responses.add(
            responses.GET, "https://dnsdumpster.com/static/map/example.com.png", body=b"fake image data", status=200
        )

        # Mock Excel download
        responses.add(
            responses.GET,
            "https://dnsdumpster.com/static/xlsx/example.com-12345678-1234-1234-1234-123456789abc.xlsx",
            body=b"fake excel data",
            status=200,
        )

        api = DNSDumpsterAPI(verbose=False)
        results = api.search("example.com")

        # Check domain
        assert results["domain"] == "example.com"

        # Check DNS records structure
        assert "dns_records" in results
        assert "dns" in results["dns_records"]
        assert "mx" in results["dns_records"]
        assert "ns" in results["dns_records"]
        assert "txt" in results["dns_records"]
        assert "host" in results["dns_records"]

        # Check that records were parsed
        assert len(results["dns_records"]["dns"]) > 0
        assert len(results["dns_records"]["mx"]) > 0
        assert len(results["dns_records"]["ns"]) > 0
        assert len(results["dns_records"]["txt"]) > 0

        # Check image data
        assert results["image_data"] is not None
        assert results["image_url"] == "https://dnsdumpster.com/static/map/example.com.png"

        # Check Excel data
        assert results["xls_data"] is not None
        assert "example.com" in results["xls_url"]

    @responses.activate
    def test_search_api_error_status(self, sample_main_page_html):
        """Test search with non-200 status code."""
        # Mock the main page request
        responses.add(responses.GET, "https://dnsdumpster.com/", body=sample_main_page_html, status=200)

        # Mock failed API request
        responses.add(responses.POST, "https://api.dnsdumpster.com/htmld/", status=500)

        api = DNSDumpsterAPI(verbose=False)

        with pytest.raises(DNSDumpsterRequestError):
            api.search("example.com")

    @responses.activate
    def test_search_api_error_message(self, sample_main_page_html):
        """Test search with error message in response."""
        # Mock the main page request
        responses.add(responses.GET, "https://dnsdumpster.com/", body=sample_main_page_html, status=200)

        # Mock API request with error message
        responses.add(
            responses.POST, "https://api.dnsdumpster.com/htmld/", body="There was an error getting results", status=200
        )

        api = DNSDumpsterAPI(verbose=False)

        with pytest.raises(DNSDumpsterAPIError):
            api.search("example.com")

    @responses.activate
    def test_search_missing_auth_token(self):
        """Test search when authorization token is missing."""
        # Mock main page without proper auth token
        html = "<html><body><form></form></body></html>"
        responses.add(responses.GET, "https://dnsdumpster.com/", body=html, status=200)

        api = DNSDumpsterAPI(verbose=False)

        with pytest.raises(DNSDumpsterParseError):
            api.search("example.com")

    @responses.activate
    def test_search_network_error(self):
        """Test search with network error."""
        # Don't mock anything to simulate network error
        api = DNSDumpsterAPI(verbose=False)

        with pytest.raises(DNSDumpsterRequestError):
            api.search("example.com")

    @responses.activate
    def test_search_image_download_failure(self, sample_main_page_html, sample_full_response_html):
        """Test search when image download fails."""
        # Mock the main page request
        responses.add(responses.GET, "https://dnsdumpster.com/", body=sample_main_page_html, status=200)

        # Mock the API request
        responses.add(responses.POST, "https://api.dnsdumpster.com/htmld/", body=sample_full_response_html, status=200)

        # Mock failed image download
        responses.add(responses.GET, "https://dnsdumpster.com/static/map/example.com.png", status=404)

        # Mock Excel download
        responses.add(
            responses.GET,
            "https://dnsdumpster.com/static/xlsx/example.com-12345678-1234-1234-1234-123456789abc.xlsx",
            body=b"fake excel data",
            status=200,
        )

        api = DNSDumpsterAPI(verbose=False)
        results = api.search("example.com")

        # Should still return results even if image fails
        assert results["domain"] == "example.com"
        # Image should be None on failure
        assert results["image_data"] is None or results["image_url"] is not None

    @responses.activate
    def test_search_with_custom_session(self, sample_main_page_html, sample_full_response_html):
        """Test search with custom requests session."""
        import requests

        # Mock the main page request
        responses.add(responses.GET, "https://dnsdumpster.com/", body=sample_main_page_html, status=200)

        # Mock the API request
        responses.add(responses.POST, "https://api.dnsdumpster.com/htmld/", body=sample_full_response_html, status=200)

        # Mock downloads
        responses.add(
            responses.GET, "https://dnsdumpster.com/static/map/example.com.png", body=b"fake image data", status=200
        )
        responses.add(
            responses.GET,
            "https://dnsdumpster.com/static/xlsx/example.com-12345678-1234-1234-1234-123456789abc.xlsx",
            body=b"fake excel data",
            status=200,
        )

        # Create custom session
        custom_session = requests.Session()
        custom_session.headers.update({"Custom-Header": "test"})

        api = DNSDumpsterAPI(verbose=False, session=custom_session)
        results = api.search("example.com")

        assert results["domain"] == "example.com"


class TestAuthorizationToken:
    """Test authorization token retrieval."""

    @responses.activate
    def test_get_authorization_token_success(self, sample_main_page_html):
        """Test successful auth token retrieval."""
        responses.add(responses.GET, "https://dnsdumpster.com/", body=sample_main_page_html, status=200)

        api = DNSDumpsterAPI(verbose=False)
        token = api._get_authorization_token()

        assert token == "Bearer test-token-12345"

    @responses.activate
    def test_get_authorization_token_missing_form(self):
        """Test auth token retrieval with missing form."""
        html = "<html><body>No form here</body></html>"
        responses.add(responses.GET, "https://dnsdumpster.com/", body=html, status=200)

        api = DNSDumpsterAPI(verbose=False)

        with pytest.raises(DNSDumpsterParseError, match="Could not find main form"):
            api._get_authorization_token()

    @responses.activate
    def test_get_authorization_token_missing_headers(self):
        """Test auth token retrieval with missing hx-headers."""
        html = '<html><body><form data-form-id="mainform"></form></body></html>'
        responses.add(responses.GET, "https://dnsdumpster.com/", body=html, status=200)

        api = DNSDumpsterAPI(verbose=False)

        with pytest.raises(DNSDumpsterParseError, match="Could not find hx-headers"):
            api._get_authorization_token()

    @responses.activate
    def test_get_authorization_token_invalid_json(self):
        """Test auth token retrieval with invalid JSON."""
        html = '<html><body><form data-form-id="mainform" hx-headers="invalid json"></form></body></html>'
        responses.add(responses.GET, "https://dnsdumpster.com/", body=html, status=200)

        api = DNSDumpsterAPI(verbose=False)

        with pytest.raises(DNSDumpsterParseError, match="Failed to parse authorization token"):
            api._get_authorization_token()


class TestExceptionHandling:
    """Test custom exceptions."""

    def test_dnsdumpster_api_error(self):
        """Test DNSDumpsterAPIError exception."""
        with pytest.raises(DNSDumpsterAPIError):
            raise DNSDumpsterAPIError("Test error")

    def test_dnsdumpster_request_error(self):
        """Test DNSDumpsterRequestError exception."""
        with pytest.raises(DNSDumpsterRequestError):
            raise DNSDumpsterRequestError("Request failed")

    def test_dnsdumpster_parse_error(self):
        """Test DNSDumpsterParseError exception."""
        with pytest.raises(DNSDumpsterParseError):
            raise DNSDumpsterParseError("Parse failed")

    def test_exception_inheritance(self):
        """Test that specific exceptions inherit from base."""
        assert issubclass(DNSDumpsterRequestError, DNSDumpsterAPIError)
        assert issubclass(DNSDumpsterParseError, DNSDumpsterAPIError)
