"""
This is the UNOFFICIAL Python API for dnsdumpster.com Website.

DNSDumpster.com offers an official API plan. This is an unofficial wrapper
that scrapes the public website and should be used responsibly.

For official API access, please visit: https://dnsdumpster.com/

Using this code, you can retrieve subdomains and DNS information.
"""

from __future__ import annotations

import base64
import html
import json
import logging
import re
import sys
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup, Tag

# Set up logging
logger = logging.getLogger(__name__)


class DNSDumpsterAPIError(Exception):
    """Base exception for DNSDumpster API errors."""

    pass


class DNSDumpsterRequestError(DNSDumpsterAPIError):
    """Exception raised when HTTP request fails."""

    pass


class DNSDumpsterParseError(DNSDumpsterAPIError):
    """Exception raised when parsing response fails."""

    pass


class DNSDumpsterAPI:
    """
    UNOFFICIAL API wrapper for dnsdumpster.com.

    This class provides methods to search for DNS records and subdomains
    by scraping the dnsdumpster.com website.

    Args:
        verbose: Enable verbose logging output.
        session: Optional requests Session object. If None, a new session is created.

    Example:
        >>> api = DNSDumpsterAPI(verbose=True)
        >>> results = api.search('example.com')
        >>> print(results['dns_records']['dns'])
    """

    BASE_URL = "https://dnsdumpster.com/"
    API_URL = "https://api.dnsdumpster.com/htmld/"

    def __init__(self, verbose: bool = False, session: Optional[requests.Session] = None):
        """Initialize the DNSDumpster API client."""
        self.verbose = verbose
        self.session = session if session is not None else requests.Session()

        # Configure logging based on verbose flag
        if verbose:
            logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
        else:
            logging.basicConfig(level=logging.WARNING)

    def _log(self, message: str) -> None:
        """
        Log a message if verbose mode is enabled.

        Args:
            message: The message to log.
        """
        if self.verbose:
            logger.info(message)

    @staticmethod
    def _extract_ip_address(td: Tag) -> str:
        """
        Extract IP address from a table cell.

        Args:
            td: BeautifulSoup Tag object representing a table cell.

        Returns:
            IP address as string, or empty string if not found.
        """
        pattern_ip = r"([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})"
        ip_matches = re.findall(pattern_ip, td.get_text())
        return ip_matches[0] if ip_matches else ""

    @staticmethod
    def _extract_reverse_dns(td: Tag) -> str:
        """
        Extract reverse DNS from a table cell.

        Args:
            td: BeautifulSoup Tag object representing a table cell.

        Returns:
            Reverse DNS as string, or empty string if not found.
        """
        reverse_dns_span = td.find("span", class_="xs-text")
        return reverse_dns_span.get_text(strip=True) if reverse_dns_span else ""

    @staticmethod
    def _extract_asn(td: Tag) -> str:
        """
        Extract ASN (Autonomous System Number) from a table cell.

        Args:
            td: BeautifulSoup Tag object representing a table cell.

        Returns:
            ASN as string with 'ASN:' prefix, or empty string if not found.
        """
        asn_text = td.get_text(separator="|", strip=True)
        asn_match = re.search(r"ASN:(\d+)", asn_text)
        return "ASN:" + asn_match.group(1) if asn_match else ""

    @staticmethod
    def _extract_subnet(td: Tag) -> str:
        """
        Extract subnet information from a table cell.

        Args:
            td: BeautifulSoup Tag object representing a table cell.

        Returns:
            Subnet as string, or empty string if not found.
        """
        subnet_span = td.find("span", class_="sm-text")
        return subnet_span.get_text(strip=True) if subnet_span else ""

    @staticmethod
    def _extract_country(td: Tag) -> str:
        """
        Extract country information from a table cell.

        Args:
            td: BeautifulSoup Tag object representing a table cell.

        Returns:
            Country as string, or empty string if not found.
        """
        country_span = td.find("span", class_="light-text")
        return country_span.get_text(strip=True) if country_span else ""

    @staticmethod
    def _extract_asn_name(td: Tag, country: str) -> str:
        """
        Extract ASN name/provider from a table cell.

        Args:
            td: BeautifulSoup Tag object representing a table cell.
            country: Country string to remove from the text.

        Returns:
            ASN name/provider as string, or empty string if not found.
        """
        provider_text = td.get_text(separator="|", strip=True)
        asn_name = provider_text.replace(country, "").replace("|", " ").strip()
        return asn_name

    def _parse_common_columns(self, tds: List[Tag], start_col: int = 1) -> Dict[str, str]:
        """
        Parse common columns (IP, ASN, Country) that appear in most record types.

        Args:
            tds: List of table cell Tags.
            start_col: Starting column index for IP column (default 1).

        Returns:
            Dictionary with parsed common fields.
        """
        data: Dict[str, str] = {}

        try:
            # IP and Reverse DNS column
            if len(tds) > start_col and tds[start_col]:
                ip_column = tds[start_col]
                data["ip"] = self._extract_ip_address(ip_column)
                data["reverse_dns"] = self._extract_reverse_dns(ip_column)
            else:
                data["ip"] = ""
                data["reverse_dns"] = ""

            # ASN and Subnet column
            if len(tds) > start_col + 1 and tds[start_col + 1]:
                asn_column = tds[start_col + 1]
                data["asn"] = self._extract_asn(asn_column)
                data["subnet"] = self._extract_subnet(asn_column)
            else:
                data["asn"] = ""
                data["subnet"] = ""

            # Provider and Country column
            if len(tds) > start_col + 2 and tds[start_col + 2]:
                provider_column = tds[start_col + 2]
                data["country"] = self._extract_country(provider_column)
                data["asn_name"] = self._extract_asn_name(provider_column, data["country"])
            else:
                data["asn_name"] = ""
                data["country"] = ""

        except Exception as e:
            self._log(f"Error parsing common columns: {e}")
            # Return partial data on error

        return data

    def retrieve_results(self, table: Tag) -> List[Dict[str, str]]:
        """
        Extract A Records (subdomains) from an HTML table.

        Args:
            table: BeautifulSoup Tag object representing the table.

        Returns:
            List of dictionaries containing subdomain information with keys:
            - host: Hostname/subdomain
            - ip: IP address
            - reverse_dns: Reverse DNS lookup
            - asn: Autonomous System Number
            - asn_name: ASN provider name
            - country: Country code/name
            - subnet: Subnet information
            - open_services: Open services/ports (if available)
            - domain: Alias for 'host' (backward compatibility)
            - as: Alias for 'asn' (backward compatibility)
            - provider: Alias for 'asn_name' (backward compatibility)
        """
        res: List[Dict[str, str]] = []
        trs = table.findAll("tr")

        for tr in trs:
            tds = tr.findAll("td")

            # Skip header rows or rows without enough columns
            if len(tds) < 4:
                continue

            try:
                data: Dict[str, str] = {}

                # Column 1: Host/Domain
                data["host"] = tds[0].get_text(strip=True) if tds[0] else ""

                # Parse common columns (IP, ASN, Country, etc.)
                common_data = self._parse_common_columns(tds, start_col=1)
                data.update(common_data)

                # Column 5: Open Services (if exists)
                if len(tds) >= 5 and tds[4]:
                    services_text = tds[4].get_text(strip=True)
                    data["open_services"] = services_text if services_text else ""
                else:
                    data["open_services"] = ""

                # Add backward-compatible keys
                data["domain"] = data["host"]
                data["as"] = data["asn"]
                data["provider"] = data["asn_name"]

                # Only add if we have at least a host or IP
                if data["host"] or data["ip"]:
                    res.append(data)

            except Exception as e:
                self._log(f"Error parsing A record row: {e}")
                continue

        return res

    def retrieve_mx_records(self, table: Tag) -> List[Dict[str, str]]:
        """
        Extract MX (Mail Exchange) Records from an HTML table.

        Args:
            table: BeautifulSoup Tag object representing the table.

        Returns:
            List of dictionaries containing MX record information with keys:
            - priority: MX priority value
            - server: Mail server hostname
            - ip: IP address
            - reverse_dns: Reverse DNS lookup
            - asn: Autonomous System Number
            - asn_name: ASN provider name
            - country: Country code/name
            - subnet: Subnet information
            - domain: Alias for 'server' (backward compatibility)
            - as: Alias for 'asn' (backward compatibility)
            - provider: Alias for 'asn_name' (backward compatibility)
        """
        res: List[Dict[str, str]] = []
        trs = table.findAll("tr")

        for tr in trs:
            tds = tr.findAll("td")

            # Skip header rows or rows without enough columns
            if len(tds) < 4:
                continue

            try:
                data: Dict[str, str] = {}

                # Column 1: Priority and Server (e.g., "10 mail.example.com")
                if tds[0]:
                    mx_text = tds[0].get_text(strip=True)
                    mx_parts = mx_text.split(None, 1)  # Split on first whitespace
                    if len(mx_parts) >= 2:
                        data["priority"] = mx_parts[0]
                        data["server"] = mx_parts[1]
                    elif len(mx_parts) == 1:
                        data["priority"] = ""
                        data["server"] = mx_parts[0]
                    else:
                        data["priority"] = ""
                        data["server"] = mx_text
                else:
                    data["priority"] = ""
                    data["server"] = ""

                # Parse common columns
                common_data = self._parse_common_columns(tds, start_col=1)
                data.update(common_data)

                # Add backward-compatible keys
                data["domain"] = data["server"]
                data["as"] = data["asn"]
                data["provider"] = data["asn_name"]

                # Only add if we have at least a server or IP
                if data["server"] or data["ip"]:
                    res.append(data)

            except Exception as e:
                self._log(f"Error parsing MX record row: {e}")
                continue

        return res

    def retrieve_ns_records(self, table: Tag) -> List[Dict[str, str]]:
        """
        Extract NS (Name Server) Records from an HTML table.

        Args:
            table: BeautifulSoup Tag object representing the table.

        Returns:
            List of dictionaries containing NS record information with keys:
            - nameserver: Nameserver hostname
            - ip: IP address
            - reverse_dns: Reverse DNS lookup
            - asn: Autonomous System Number
            - asn_name: ASN provider name
            - country: Country code/name
            - subnet: Subnet information
            - domain: Alias for 'nameserver' (backward compatibility)
            - as: Alias for 'asn' (backward compatibility)
            - provider: Alias for 'asn_name' (backward compatibility)
        """
        res: List[Dict[str, str]] = []
        trs = table.findAll("tr")

        for tr in trs:
            tds = tr.findAll("td")

            # Skip header rows or rows without enough columns
            if len(tds) < 4:
                continue

            try:
                data: Dict[str, str] = {}

                # Column 1: Nameserver
                data["nameserver"] = tds[0].get_text(strip=True) if tds[0] else ""

                # Parse common columns
                common_data = self._parse_common_columns(tds, start_col=1)
                data.update(common_data)

                # Add backward-compatible keys
                data["domain"] = data["nameserver"]
                data["as"] = data["asn"]
                data["provider"] = data["asn_name"]

                # Only add if we have at least a nameserver or IP
                if data["nameserver"] or data["ip"]:
                    res.append(data)

            except Exception as e:
                self._log(f"Error parsing NS record row: {e}")
                continue

        return res

    def retrieve_txt_record(self, table: Tag) -> List[str]:
        """
        Extract TXT Records from an HTML table.

        Args:
            table: BeautifulSoup Tag object representing the table.

        Returns:
            List of text content from each table cell.
        """
        res: List[str] = []

        try:
            trs = table.findAll("tr")
            for tr in trs:
                tds = tr.findAll("td")
                for td in tds:
                    text = td.get_text(strip=True)
                    if text:
                        res.append(text)
        except Exception as e:
            self._log(f"Error parsing TXT records: {e}")

        return res

    def find_table_by_heading(self, soup: BeautifulSoup, heading_text: str) -> Optional[Tag]:
        """
        Find an HTML table by looking for a preceding paragraph tag with specific text.

        Args:
            soup: BeautifulSoup object representing the HTML document.
            heading_text: Text to search for in paragraph tags.

        Returns:
            BeautifulSoup Tag object representing the table, or None if not found.
        """
        try:
            # Find all paragraph tags
            paragraphs = soup.find_all("p")

            for p in paragraphs:
                # Check if this paragraph contains the heading text
                if heading_text.lower() in p.get_text(strip=True).lower():
                    # Find the next table after this paragraph
                    next_table = p.find_next("table")
                    if next_table:
                        return next_table
        except Exception as e:
            self._log(f'Error finding table for heading "{heading_text}": {e}')

        return None

    def _get_authorization_token(self) -> str:
        """
        Retrieve authorization token from DNSDumpster main page.

        Returns:
            Authorization token string.

        Raises:
            DNSDumpsterRequestError: If unable to retrieve the token.
        """
        try:
            req = self.session.get(self.BASE_URL)
            req.raise_for_status()

            soup = BeautifulSoup(req.content, "html.parser")
            form = soup.find("form", attrs={"data-form-id": "mainform"})

            if not form:
                raise DNSDumpsterParseError("Could not find main form on DNSDumpster page")

            hx_headers = form.get("hx-headers")
            if not hx_headers:
                raise DNSDumpsterParseError("Could not find hx-headers attribute in form")

            unescaped = html.unescape(hx_headers)
            headers_dict = json.loads(unescaped)
            auth_token = headers_dict.get("Authorization")

            if not auth_token:
                raise DNSDumpsterParseError("Could not extract authorization token")

            self._log(f"Retrieved access token: {auth_token}")
            return auth_token

        except requests.RequestException as e:
            raise DNSDumpsterRequestError(f"Failed to retrieve authorization token: {e}")
        except (ValueError, json.JSONDecodeError) as e:
            raise DNSDumpsterParseError(f"Failed to parse authorization token: {e}")

    def search(self, domain: str) -> Dict[str, Any]:
        """
        Search for DNS records and subdomains for a given domain.

        This method queries dnsdumpster.com and retrieves:
        - A Records (subdomains)
        - MX Records (mail servers)
        - NS Records (name servers)
        - TXT Records
        - Network mapping image
        - Excel file with detailed results

        Args:
            domain: The domain name to search for (e.g., 'example.com').

        Returns:
            Dictionary containing:
            - domain: The queried domain
            - dns_records: Dictionary with 'dns', 'mx', 'ns', 'txt', 'host' keys
            - image_data: Base64 encoded network map image (or None)
            - image_url: URL to the network map image (or None)
            - xls_data: Base64 encoded Excel file (or None)
            - xls_url: URL to the Excel file (or None)

        Raises:
            DNSDumpsterRequestError: If HTTP request fails.
            DNSDumpsterParseError: If parsing the response fails.
        """
        # Get authorization token
        auth_token = self._get_authorization_token()

        # Prepare request headers and data
        headers = {
            "Referer": self.BASE_URL,
            "Origin": self.BASE_URL,
            "Authorization": auth_token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        }
        data = {"target": domain}

        # Make the search request
        try:
            req = self.session.post(self.API_URL, data=data, headers=headers)

            if req.status_code != 200:
                raise DNSDumpsterRequestError(f"Unexpected status code from {self.API_URL}: {req.status_code}")

            content = req.content.decode("utf-8")
            if "There was an error getting results" in content:
                raise DNSDumpsterAPIError("There was an error getting results from DNSDumpster")

        except requests.RequestException as e:
            raise DNSDumpsterRequestError(f"Failed to perform search: {e}")

        # Parse the response
        soup = BeautifulSoup(req.content, "html.parser")

        res: Dict[str, Any] = {"domain": domain, "dns_records": {}}

        # Parse DNS records
        res["dns_records"] = self._parse_dns_records(soup)

        # Retrieve network map image
        res["image_data"], res["image_url"] = self._retrieve_image(soup, domain)

        # Retrieve Excel file
        res["xls_data"], res["xls_url"] = self._retrieve_excel(soup, domain, req.content.decode("utf-8"))

        return res

    def _parse_dns_records(self, soup: BeautifulSoup) -> Dict[str, List]:
        """
        Parse all DNS record types from the HTML soup.

        Args:
            soup: BeautifulSoup object representing the response HTML.

        Returns:
            Dictionary with keys 'dns', 'mx', 'ns', 'txt', 'host' containing parsed records.
        """
        dns_records: Dict[str, List] = {}

        # Find tables by their heading paragraphs
        a_records_table = self.find_table_by_heading(soup, "A Records") or self.find_table_by_heading(
            soup, "subdomains from dataset"
        )
        mx_records_table = self.find_table_by_heading(soup, "MX Records")
        ns_records_table = self.find_table_by_heading(soup, "NS Records")
        txt_records_table = self.find_table_by_heading(soup, "TXT Records")

        # Parse A Records (DNS/subdomains)
        if a_records_table:
            dns_records["dns"] = self.retrieve_results(a_records_table)
            self._log(f'Found {len(dns_records["dns"])} A records')
        else:
            dns_records["dns"] = []
            self._log("No A records table found")

        # Parse MX Records
        if mx_records_table:
            dns_records["mx"] = self.retrieve_mx_records(mx_records_table)
            self._log(f'Found {len(dns_records["mx"])} MX records')
        else:
            dns_records["mx"] = []
            self._log("No MX records table found")

        # Parse NS Records
        if ns_records_table:
            dns_records["ns"] = self.retrieve_ns_records(ns_records_table)
            self._log(f'Found {len(dns_records["ns"])} NS records')
        else:
            dns_records["ns"] = []
            self._log("No NS records table found")

        # Parse TXT Records
        if txt_records_table:
            dns_records["txt"] = self.retrieve_txt_record(txt_records_table)
            self._log(f'Found {len(dns_records["txt"])} TXT records')
        else:
            dns_records["txt"] = []
            self._log("No TXT records table found")

        # For backward compatibility, also store NS records as 'host'
        dns_records["host"] = dns_records["ns"]

        return dns_records

    def _retrieve_image(self, soup: BeautifulSoup, domain: str) -> tuple[Optional[bytes], Optional[str]]:
        """
        Retrieve the network mapping image.

        Args:
            soup: BeautifulSoup object representing the response HTML.
            domain: The queried domain.

        Returns:
            Tuple of (base64 encoded image data, image URL).
            Both can be None if retrieval fails.
        """
        image_data = None
        image_url = None

        try:
            logo_img = soup.find("img", alt="Logo")
            if logo_img and logo_img.get("src"):
                image_url = logo_img.get("src")
                # If it's a relative URL, make it absolute
                if image_url.startswith("/"):
                    image_url = "https://dnsdumpster.com" + image_url
                elif not image_url.startswith("http"):
                    image_url = "https://dnsdumpster.com/" + image_url

                self._log(f"Found image URL: {image_url}")
                image_data = base64.b64encode(self.session.get(image_url).content)
            else:
                # Fallback to old method
                self._log("Logo img not found, trying fallback method")
                tmp_url = f"https://dnsdumpster.com/static/map/{domain}.png"
                image_data = base64.b64encode(self.session.get(tmp_url).content)
                image_url = tmp_url
        except Exception as e:
            self._log(f"Error retrieving image: {e}")

        return image_data, image_url

    def _retrieve_excel(self, soup: BeautifulSoup, domain: str, content: str) -> tuple[Optional[bytes], Optional[str]]:
        """
        Retrieve the Excel file with detailed results.

        Args:
            soup: BeautifulSoup object representing the response HTML.
            domain: The queried domain.
            content: Raw HTML content as string.

        Returns:
            Tuple of (base64 encoded Excel data, Excel URL).
            Both can be None if retrieval fails.
        """
        xls_data = None
        xls_url = None

        try:
            # Find the download link
            download_links = soup.find_all("a")
            for link in download_links:
                link_text = link.get_text(strip=True).lower()
                if "download" in link_text and "xlsx" in link_text:
                    xls_url = link.get("href")
                    if xls_url:
                        # If it's a relative URL, make it absolute
                        if xls_url.startswith("/"):
                            xls_url = "https://dnsdumpster.com" + xls_url
                        elif not xls_url.startswith("http"):
                            xls_url = "https://dnsdumpster.com/" + xls_url

                        self._log(f"Found Excel URL: {xls_url}")
                        xls_data = base64.b64encode(self.session.get(xls_url).content)
                        break

            # Fallback to pattern matching if the link wasn't found
            if not xls_url:
                self._log("Download link not found, trying fallback method")
                pattern = r"/static/xlsx/" + re.escape(domain) + r"-[a-f0-9\-]{36}\.xlsx"
                xls_matches = re.findall(pattern, content)
                if xls_matches:
                    xls_url = "https://dnsdumpster.com" + xls_matches[0]
                    xls_data = base64.b64encode(self.session.get(xls_url).content)
        except Exception as err:
            self._log(f"Error retrieving Excel file: {err}")

        return xls_data, xls_url
