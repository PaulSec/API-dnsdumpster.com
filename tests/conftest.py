"""Pytest configuration and fixtures for DNSDumpster API tests."""

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def sample_a_records_html():
    """Sample HTML for A Records table."""
    return """
    <table>
        <tr>
            <td>subdomain.example.com</td>
            <td>192.0.2.1<br><span class="xs-text">ex1.reverse.dns.com</span></td>
            <td>ASN:12345<br><span class="sm-text">192.0.2.0/24</span></td>
            <td>Example Provider<br><span class="light-text">United States</span></td>
            <td>80, 443</td>
        </tr>
        <tr>
            <td>api.example.com</td>
            <td>192.0.2.2<br><span class="xs-text">ex2.reverse.dns.com</span></td>
            <td>ASN:12345<br><span class="sm-text">192.0.2.0/24</span></td>
            <td>Example Provider<br><span class="light-text">United States</span></td>
            <td>443</td>
        </tr>
    </table>
    """


@pytest.fixture
def sample_mx_records_html():
    """Sample HTML for MX Records table."""
    return """
    <table>
        <tr>
            <td>10 mail1.example.com</td>
            <td>198.51.100.1<br><span class="xs-text">mail1.reverse.dns.com</span></td>
            <td>ASN:23456<br><span class="sm-text">198.51.100.0/24</span></td>
            <td>Mail Provider<br><span class="light-text">Germany</span></td>
        </tr>
        <tr>
            <td>20 mail2.example.com</td>
            <td>198.51.100.2<br><span class="xs-text">mail2.reverse.dns.com</span></td>
            <td>ASN:23456<br><span class="sm-text">198.51.100.0/24</span></td>
            <td>Mail Provider<br><span class="light-text">Germany</span></td>
        </tr>
    </table>
    """


@pytest.fixture
def sample_ns_records_html():
    """Sample HTML for NS Records table."""
    return """
    <table>
        <tr>
            <td>ns1.example.com</td>
            <td>203.0.113.1<br><span class="xs-text">ns1.reverse.dns.com</span></td>
            <td>ASN:34567<br><span class="sm-text">203.0.113.0/24</span></td>
            <td>DNS Provider<br><span class="light-text">United Kingdom</span></td>
        </tr>
        <tr>
            <td>ns2.example.com</td>
            <td>203.0.113.2<br><span class="xs-text">ns2.reverse.dns.com</span></td>
            <td>ASN:34567<br><span class="sm-text">203.0.113.0/24</span></td>
            <td>DNS Provider<br><span class="light-text">United Kingdom</span></td>
        </tr>
    </table>
    """


@pytest.fixture
def sample_txt_records_html():
    """Sample HTML for TXT Records table."""
    return """
    <table>
        <tr>
            <td>v=spf1 include:_spf.example.com ~all</td>
        </tr>
        <tr>
            <td>google-site-verification=abcdef123456</td>
        </tr>
    </table>
    """


@pytest.fixture
def sample_full_response_html():
    """Sample full HTML response from DNSDumpster."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>DNSDumpster</title></head>
    <body>
        <p>A Records found</p>
        <table>
            <tr>
                <td>test.example.com</td>
                <td>192.0.2.100<br><span class="xs-text">reverse.test.com</span></td>
                <td>ASN:11111<br><span class="sm-text">192.0.2.0/24</span></td>
                <td>Test Provider<br><span class="light-text">US</span></td>
            </tr>
        </table>
        
        <p>MX Records</p>
        <table>
            <tr>
                <td>10 mx.example.com</td>
                <td>198.51.100.10<br><span class="xs-text">mx.reverse.com</span></td>
                <td>ASN:22222<br><span class="sm-text">198.51.100.0/24</span></td>
                <td>MX Provider<br><span class="light-text">DE</span></td>
            </tr>
        </table>
        
        <p>NS Records</p>
        <table>
            <tr>
                <td>ns.example.com</td>
                <td>203.0.113.10<br><span class="xs-text">ns.reverse.com</span></td>
                <td>ASN:33333<br><span class="sm-text">203.0.113.0/24</span></td>
                <td>NS Provider<br><span class="light-text">UK</span></td>
            </tr>
        </table>
        
        <p>TXT Records</p>
        <table>
            <tr>
                <td>v=spf1 include:_spf.example.com ~all</td>
            </tr>
        </table>
        
        <img alt="Logo" src="/static/map/example.com.png">
        <a href="/static/xlsx/example.com-12345678-1234-1234-1234-123456789abc.xlsx">Download xlsx</a>
    </body>
    </html>
    """


@pytest.fixture
def sample_main_page_html():
    """Sample HTML for the main DNSDumpster page with auth token."""
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <form data-form-id="mainform" hx-headers='{"Authorization": "Bearer test-token-12345"}'>
            <input type="text" name="target">
        </form>
    </body>
    </html>
    """


@pytest.fixture
def empty_table_html():
    """Empty table HTML for testing edge cases."""
    return """
    <table>
        <tr>
            <th>Header 1</th>
            <th>Header 2</th>
        </tr>
    </table>
    """


@pytest.fixture
def malformed_table_html():
    """Malformed table HTML for testing error handling."""
    return """
    <table>
        <tr>
            <td>incomplete</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
        </tr>
    </table>
    """
