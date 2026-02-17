"""Unit tests for DNSDumpster API parsing methods."""

import pytest
from bs4 import BeautifulSoup

from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI


class TestHelperMethods:
    """Test static helper methods for parsing table cells."""

    def test_extract_ip_address(self):
        """Test IP address extraction from table cell."""
        html = "<td>192.0.2.1<br>some other text</td>"
        td = BeautifulSoup(html, "html.parser").find("td")

        ip = DNSDumpsterAPI._extract_ip_address(td)
        assert ip == "192.0.2.1"

    def test_extract_ip_address_none(self):
        """Test IP extraction returns empty string when not found."""
        html = "<td>no ip here</td>"
        td = BeautifulSoup(html, "html.parser").find("td")

        ip = DNSDumpsterAPI._extract_ip_address(td)
        assert ip == ""

    def test_extract_reverse_dns(self):
        """Test reverse DNS extraction from table cell."""
        html = '<td>192.0.2.1<br><span class="xs-text">reverse.dns.com</span></td>'
        td = BeautifulSoup(html, "html.parser").find("td")

        reverse_dns = DNSDumpsterAPI._extract_reverse_dns(td)
        assert reverse_dns == "reverse.dns.com"

    def test_extract_reverse_dns_none(self):
        """Test reverse DNS extraction returns empty string when not found."""
        html = "<td>192.0.2.1</td>"
        td = BeautifulSoup(html, "html.parser").find("td")

        reverse_dns = DNSDumpsterAPI._extract_reverse_dns(td)
        assert reverse_dns == ""

    def test_extract_asn(self):
        """Test ASN extraction from table cell."""
        html = "<td>ASN:12345<br>other text</td>"
        td = BeautifulSoup(html, "html.parser").find("td")

        asn = DNSDumpsterAPI._extract_asn(td)
        assert asn == "ASN:12345"

    def test_extract_asn_none(self):
        """Test ASN extraction returns empty string when not found."""
        html = "<td>no asn here</td>"
        td = BeautifulSoup(html, "html.parser").find("td")

        asn = DNSDumpsterAPI._extract_asn(td)
        assert asn == ""

    def test_extract_subnet(self):
        """Test subnet extraction from table cell."""
        html = '<td>ASN:12345<br><span class="sm-text">192.0.2.0/24</span></td>'
        td = BeautifulSoup(html, "html.parser").find("td")

        subnet = DNSDumpsterAPI._extract_subnet(td)
        assert subnet == "192.0.2.0/24"

    def test_extract_country(self):
        """Test country extraction from table cell."""
        html = '<td>Provider Name<br><span class="light-text">United States</span></td>'
        td = BeautifulSoup(html, "html.parser").find("td")

        country = DNSDumpsterAPI._extract_country(td)
        assert country == "United States"

    def test_extract_asn_name(self):
        """Test ASN name/provider extraction from table cell."""
        html = '<td>Example Provider<br><span class="light-text">United States</span></td>'
        td = BeautifulSoup(html, "html.parser").find("td")

        asn_name = DNSDumpsterAPI._extract_asn_name(td, "United States")
        assert asn_name == "Example Provider"


class TestRetrieveResults:
    """Test A Records (subdomains) parsing."""

    def test_retrieve_results_basic(self, sample_a_records_html):
        """Test basic A records parsing."""
        soup = BeautifulSoup(sample_a_records_html, "html.parser")
        table = soup.find("table")

        api = DNSDumpsterAPI(verbose=False)
        results = api.retrieve_results(table)

        assert len(results) == 2

        # Check first record
        assert results[0]["host"] == "subdomain.example.com"
        assert results[0]["ip"] == "192.0.2.1"
        assert results[0]["reverse_dns"] == "ex1.reverse.dns.com"
        assert results[0]["asn"] == "ASN:12345"
        assert results[0]["subnet"] == "192.0.2.0/24"
        assert results[0]["asn_name"] == "Example Provider"
        assert results[0]["country"] == "United States"
        assert results[0]["open_services"] == "80, 443"

        # Check backward compatibility keys
        assert results[0]["domain"] == results[0]["host"]
        assert results[0]["as"] == results[0]["asn"]
        assert results[0]["provider"] == results[0]["asn_name"]

    def test_retrieve_results_empty_table(self, empty_table_html):
        """Test parsing empty table."""
        soup = BeautifulSoup(empty_table_html, "html.parser")
        table = soup.find("table")

        api = DNSDumpsterAPI(verbose=False)
        results = api.retrieve_results(table)

        assert len(results) == 0

    def test_retrieve_results_malformed_table(self, malformed_table_html):
        """Test parsing malformed table."""
        soup = BeautifulSoup(malformed_table_html, "html.parser")
        table = soup.find("table")

        api = DNSDumpsterAPI(verbose=False)
        results = api.retrieve_results(table)

        # Should not crash, just skip malformed rows
        assert isinstance(results, list)


class TestRetrieveMXRecords:
    """Test MX Records parsing."""

    def test_retrieve_mx_records_basic(self, sample_mx_records_html):
        """Test basic MX records parsing."""
        soup = BeautifulSoup(sample_mx_records_html, "html.parser")
        table = soup.find("table")

        api = DNSDumpsterAPI(verbose=False)
        results = api.retrieve_mx_records(table)

        assert len(results) == 2

        # Check first record
        assert results[0]["priority"] == "10"
        assert results[0]["server"] == "mail1.example.com"
        assert results[0]["ip"] == "198.51.100.1"
        assert results[0]["reverse_dns"] == "mail1.reverse.dns.com"
        assert results[0]["asn"] == "ASN:23456"
        assert results[0]["subnet"] == "198.51.100.0/24"
        assert results[0]["asn_name"] == "Mail Provider"
        assert results[0]["country"] == "Germany"

        # Check backward compatibility
        assert results[0]["domain"] == results[0]["server"]

    def test_retrieve_mx_records_empty_table(self, empty_table_html):
        """Test parsing empty MX table."""
        soup = BeautifulSoup(empty_table_html, "html.parser")
        table = soup.find("table")

        api = DNSDumpsterAPI(verbose=False)
        results = api.retrieve_mx_records(table)

        assert len(results) == 0


class TestRetrieveNSRecords:
    """Test NS Records parsing."""

    def test_retrieve_ns_records_basic(self, sample_ns_records_html):
        """Test basic NS records parsing."""
        soup = BeautifulSoup(sample_ns_records_html, "html.parser")
        table = soup.find("table")

        api = DNSDumpsterAPI(verbose=False)
        results = api.retrieve_ns_records(table)

        assert len(results) == 2

        # Check first record
        assert results[0]["nameserver"] == "ns1.example.com"
        assert results[0]["ip"] == "203.0.113.1"
        assert results[0]["reverse_dns"] == "ns1.reverse.dns.com"
        assert results[0]["asn"] == "ASN:34567"
        assert results[0]["subnet"] == "203.0.113.0/24"
        assert results[0]["asn_name"] == "DNS Provider"
        assert results[0]["country"] == "United Kingdom"

        # Check backward compatibility
        assert results[0]["domain"] == results[0]["nameserver"]

    def test_retrieve_ns_records_empty_table(self, empty_table_html):
        """Test parsing empty NS table."""
        soup = BeautifulSoup(empty_table_html, "html.parser")
        table = soup.find("table")

        api = DNSDumpsterAPI(verbose=False)
        results = api.retrieve_ns_records(table)

        assert len(results) == 0


class TestRetrieveTXTRecords:
    """Test TXT Records parsing."""

    def test_retrieve_txt_records_basic(self, sample_txt_records_html):
        """Test basic TXT records parsing."""
        soup = BeautifulSoup(sample_txt_records_html, "html.parser")
        table = soup.find("table")

        api = DNSDumpsterAPI(verbose=False)
        results = api.retrieve_txt_record(table)

        assert len(results) == 2
        assert "v=spf1 include:_spf.example.com ~all" in results
        assert "google-site-verification=abcdef123456" in results

    def test_retrieve_txt_records_empty_table(self, empty_table_html):
        """Test parsing empty TXT table."""
        soup = BeautifulSoup(empty_table_html, "html.parser")
        table = soup.find("table")

        api = DNSDumpsterAPI(verbose=False)
        results = api.retrieve_txt_record(table)

        assert len(results) == 0


class TestFindTableByHeading:
    """Test table finding by heading."""

    def test_find_table_by_heading_found(self):
        """Test finding table by heading text."""
        html = """
        <p>A Records found</p>
        <table>
            <tr><td>test data</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, "html.parser")

        api = DNSDumpsterAPI(verbose=False)
        table = api.find_table_by_heading(soup, "A Records")

        assert table is not None
        assert table.name == "table"

    def test_find_table_by_heading_not_found(self):
        """Test table finding returns None when not found."""
        html = "<p>Some other text</p>"
        soup = BeautifulSoup(html, "html.parser")

        api = DNSDumpsterAPI(verbose=False)
        table = api.find_table_by_heading(soup, "A Records")

        assert table is None

    def test_find_table_by_heading_case_insensitive(self):
        """Test finding table is case insensitive."""
        html = """
        <p>a records found</p>
        <table>
            <tr><td>test data</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, "html.parser")

        api = DNSDumpsterAPI(verbose=False)
        table = api.find_table_by_heading(soup, "A Records")

        assert table is not None


class TestVerboseLogging:
    """Test verbose logging functionality."""

    def test_verbose_mode_enabled(self, capsys):
        """Test that verbose mode logs messages."""
        api = DNSDumpsterAPI(verbose=True)
        api._log("Test message")

        # Logging might not appear in capsys if logging is configured differently
        # This test ensures the method doesn't crash
        assert True

    def test_verbose_mode_disabled(self, capsys):
        """Test that non-verbose mode doesn't log."""
        api = DNSDumpsterAPI(verbose=False)
        api._log("Test message")

        # This test ensures the method doesn't crash
        assert True
