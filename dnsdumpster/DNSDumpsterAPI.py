"""
This is the (unofficial) Python API for dnsdumpster.com Website.
Using this code, you can retrieve subdomains

"""

from __future__ import print_function
import requests
import re
import sys
import base64
import html
import json

from bs4 import BeautifulSoup


class DNSDumpsterAPI(object):

    """DNSDumpsterAPI Main Handler"""

    def __init__(self, verbose=False, session=None):
        self.verbose = verbose
        if not session:
            self.session = requests.Session()
        else:
            self.session = session

    def display_message(self, s):
        if self.verbose:
            print('[verbose] %s' % s)

    def retrieve_results(self, table):
        """
        Extract A Records (subdomains) from the table.
        Returns list of dictionaries with: host, ip, reverse_dns, asn, asn_name, country, subnet, open_services
        """
        res = []
        trs = table.findAll('tr')
        
        for tr in trs:
            tds = tr.findAll('td')
            
            # Skip header rows or rows without enough columns
            if len(tds) < 4:
                continue
                
            try:
                data = {}
                
                # Column 1: Host/Domain
                if tds[0]:
                    host_text = tds[0].get_text(strip=True)
                    data['host'] = host_text if host_text else ''
                else:
                    data['host'] = ''
                
                # Column 2: IP and Reverse DNS
                if tds[1]:
                    ip_column = tds[1]
                    # Extract IP address
                    pattern_ip = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
                    ip_matches = re.findall(pattern_ip, ip_column.get_text())
                    data['ip'] = ip_matches[0] if ip_matches else ''
                    
                    # Extract reverse DNS from span with class xs-text
                    reverse_dns_span = ip_column.find('span', class_='xs-text')
                    data['reverse_dns'] = reverse_dns_span.get_text(strip=True) if reverse_dns_span else ''
                else:
                    data['ip'] = ''
                    data['reverse_dns'] = ''
                
                # Column 3: ASN and Subnet
                if tds[2]:
                    asn_column = tds[2]
                    asn_text = asn_column.get_text(separator='|', strip=True)
                    
                    # Extract ASN (format: ASN:396982)
                    asn_match = re.search(r'ASN:(\d+)', asn_text)
                    data['asn'] = 'ASN:' + asn_match.group(1) if asn_match else ''
                    
                    # Extract subnet (usually in sm-text span)
                    subnet_span = asn_column.find('span', class_='sm-text')
                    data['subnet'] = subnet_span.get_text(strip=True) if subnet_span else ''
                else:
                    data['asn'] = ''
                    data['subnet'] = ''
                
                # Column 4: ASN Name and Country
                if tds[3]:
                    provider_column = tds[3]
                    provider_text = provider_column.get_text(separator='|', strip=True)
                    
                    # Extract country (usually in light-text span)
                    country_span = provider_column.find('span', class_='light-text')
                    data['country'] = country_span.get_text(strip=True) if country_span else ''
                    
                    # ASN name is the remaining text
                    asn_name = provider_text.replace(data['country'], '').replace('|', ' ').strip()
                    data['asn_name'] = asn_name
                else:
                    data['asn_name'] = ''
                    data['country'] = ''
                
                # Column 5: Open Services (if exists)
                if len(tds) >= 5 and tds[4]:
                    services_text = tds[4].get_text(strip=True)
                    data['open_services'] = services_text if services_text else ''
                else:
                    data['open_services'] = ''
                
                # Add backward-compatible keys for old API format
                data['domain'] = data['host']
                data['as'] = data['asn']
                data['provider'] = data['asn_name']
                
                # Only add if we have at least a host or IP
                if data['host'] or data['ip']:
                    res.append(data)
                    
            except Exception as e:
                # Log error if verbose, but continue processing
                if self.verbose:
                    print(f'[verbose] Error parsing A record row: {e}')
                continue
                
        return res

    def retrieve_mx_records(self, table):
        """
        Extract MX Records from the table.
        Returns list of dictionaries with: priority, server, ip, reverse_dns, asn, asn_name, country, subnet
        """
        res = []
        trs = table.findAll('tr')
        
        for tr in trs:
            tds = tr.findAll('td')
            
            # Skip header rows or rows without enough columns
            if len(tds) < 4:
                continue
                
            try:
                data = {}
                
                # Column 1: Priority and Server (e.g., "10 mail.example.com")
                if tds[0]:
                    mx_text = tds[0].get_text(strip=True)
                    mx_parts = mx_text.split(None, 1)  # Split on first whitespace
                    if len(mx_parts) >= 2:
                        data['priority'] = mx_parts[0]
                        data['server'] = mx_parts[1]
                    elif len(mx_parts) == 1:
                        data['priority'] = ''
                        data['server'] = mx_parts[0]
                    else:
                        data['priority'] = ''
                        data['server'] = mx_text
                else:
                    data['priority'] = ''
                    data['server'] = ''
                
                # Column 2: IP and Reverse DNS
                if tds[1]:
                    ip_column = tds[1]
                    pattern_ip = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
                    ip_matches = re.findall(pattern_ip, ip_column.get_text())
                    data['ip'] = ip_matches[0] if ip_matches else ''
                    
                    reverse_dns_span = ip_column.find('span', class_='xs-text')
                    data['reverse_dns'] = reverse_dns_span.get_text(strip=True) if reverse_dns_span else ''
                else:
                    data['ip'] = ''
                    data['reverse_dns'] = ''
                
                # Column 3: ASN and Subnet
                if tds[2]:
                    asn_column = tds[2]
                    asn_text = asn_column.get_text(separator='|', strip=True)
                    
                    asn_match = re.search(r'ASN:(\d+)', asn_text)
                    data['asn'] = 'ASN:' + asn_match.group(1) if asn_match else ''
                    
                    subnet_span = asn_column.find('span', class_='sm-text')
                    data['subnet'] = subnet_span.get_text(strip=True) if subnet_span else ''
                else:
                    data['asn'] = ''
                    data['subnet'] = ''
                
                # Column 4: ASN Name and Country
                if tds[3]:
                    provider_column = tds[3]
                    provider_text = provider_column.get_text(separator='|', strip=True)
                    
                    country_span = provider_column.find('span', class_='light-text')
                    data['country'] = country_span.get_text(strip=True) if country_span else ''
                    
                    asn_name = provider_text.replace(data['country'], '').replace('|', ' ').strip()
                    data['asn_name'] = asn_name
                else:
                    data['asn_name'] = ''
                    data['country'] = ''
                
                # Add backward-compatible keys for old API format
                data['domain'] = data['server']
                data['as'] = data['asn']
                data['provider'] = data['asn_name']
                
                # Only add if we have at least a server or IP
                if data['server'] or data['ip']:
                    res.append(data)
                    
            except Exception as e:
                if self.verbose:
                    print(f'[verbose] Error parsing MX record row: {e}')
                continue
                
        return res

    def retrieve_ns_records(self, table):
        """
        Extract NS Records from the table.
        Returns list of dictionaries with: nameserver, ip, reverse_dns, asn, asn_name, country, subnet
        """
        res = []
        trs = table.findAll('tr')
        
        for tr in trs:
            tds = tr.findAll('td')
            
            # Skip header rows or rows without enough columns
            if len(tds) < 4:
                continue
                
            try:
                data = {}
                
                # Column 1: Nameserver
                if tds[0]:
                    nameserver_text = tds[0].get_text(strip=True)
                    data['nameserver'] = nameserver_text if nameserver_text else ''
                else:
                    data['nameserver'] = ''
                
                # Column 2: IP and Reverse DNS
                if tds[1]:
                    ip_column = tds[1]
                    pattern_ip = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
                    ip_matches = re.findall(pattern_ip, ip_column.get_text())
                    data['ip'] = ip_matches[0] if ip_matches else ''
                    
                    reverse_dns_span = ip_column.find('span', class_='xs-text')
                    data['reverse_dns'] = reverse_dns_span.get_text(strip=True) if reverse_dns_span else ''
                else:
                    data['ip'] = ''
                    data['reverse_dns'] = ''
                
                # Column 3: ASN and Subnet
                if tds[2]:
                    asn_column = tds[2]
                    asn_text = asn_column.get_text(separator='|', strip=True)
                    
                    asn_match = re.search(r'ASN:(\d+)', asn_text)
                    data['asn'] = 'ASN:' + asn_match.group(1) if asn_match else ''
                    
                    subnet_span = asn_column.find('span', class_='sm-text')
                    data['subnet'] = subnet_span.get_text(strip=True) if subnet_span else ''
                else:
                    data['asn'] = ''
                    data['subnet'] = ''
                
                # Column 4: ASN Name and Country
                if tds[3]:
                    provider_column = tds[3]
                    provider_text = provider_column.get_text(separator='|', strip=True)
                    
                    country_span = provider_column.find('span', class_='light-text')
                    data['country'] = country_span.get_text(strip=True) if country_span else ''
                    
                    asn_name = provider_text.replace(data['country'], '').replace('|', ' ').strip()
                    data['asn_name'] = asn_name
                else:
                    data['asn_name'] = ''
                    data['country'] = ''
                
                # Add backward-compatible keys for old API format
                data['domain'] = data['nameserver']
                data['as'] = data['asn']
                data['provider'] = data['asn_name']
                
                # Only add if we have at least a nameserver or IP
                if data['nameserver'] or data['ip']:
                    res.append(data)
                    
            except Exception as e:
                if self.verbose:
                    print(f'[verbose] Error parsing NS record row: {e}')
                continue
                
        return res

    def retrieve_txt_record(self, table):
        """
        Extract TXT Records from the table.
        Returns list of text content from each cell
        """
        res = []
        
        try:
            trs = table.findAll('tr')
            for tr in trs:
                tds = tr.findAll('td')
                for td in tds:
                    text = td.get_text(strip=True)
                    if text:
                        res.append(text)
        except Exception as e:
            if self.verbose:
                print(f'[verbose] Error parsing TXT records: {e}')
                
        return res
    
    def find_table_by_heading(self, soup, heading_text):
        """
        Find a table by looking for a preceding <p> tag with specific text.
        Returns the table element or None if not found.
        """
        try:
            # Find all paragraph tags
            paragraphs = soup.find_all('p')
            
            for p in paragraphs:
                # Check if this paragraph contains the heading text
                if heading_text.lower() in p.get_text(strip=True).lower():
                    # Find the next table after this paragraph
                    next_table = p.find_next('table')
                    if next_table:
                        return next_table
        except Exception as e:
            if self.verbose:
                print(f'[verbose] Error finding table for heading "{heading_text}": {e}')
                
        return None


    def search(self, domain):
        dnsdumpster_url = 'https://dnsdumpster.com/'
        dnsdumpster_api_url = 'https://api.dnsdumpster.com/htmld/'

        req = self.session.get(dnsdumpster_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        form = soup.find('form', attrs={'data-form-id': 'mainform'})
        hx_headers = form.get('hx-headers')
        unescaped = html.unescape(hx_headers)
        headers_dict = json.loads(unescaped)
        auth_token = headers_dict.get("Authorization")

        self.display_message('Retrievedddd access token: %s' % auth_token)

        headers = {'Referer': dnsdumpster_url, 'Origin': dnsdumpster_url, 'Authorization': auth_token, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'}
        data = {'target': domain}
        req = self.session.post(dnsdumpster_api_url, data=data, headers=headers)

        if req.status_code != 200:
            print(
                "Unexpected status code from {url}: {code}".format(
                    url=dnsdumpster_url, code=req.status_code),
                file=sys.stderr,
            )
            return []

        if 'There was an error getting results' in req.content.decode('utf-8'):
            print("There was an error getting results", file=sys.stderr)
            return []

        soup = BeautifulSoup(req.content, 'html.parser')
        
        res = {}
        res['domain'] = domain
        res['dns_records'] = {}
        
        # Find tables by their heading paragraphs
        a_records_table = self.find_table_by_heading(soup, 'A Records') or self.find_table_by_heading(soup, 'subdomains from dataset')
        mx_records_table = self.find_table_by_heading(soup, 'MX Records')
        ns_records_table = self.find_table_by_heading(soup, 'NS Records')
        txt_records_table = self.find_table_by_heading(soup, 'TXT Records')
        
        # Parse A Records (DNS/subdomains)
        if a_records_table:
            res['dns_records']['dns'] = self.retrieve_results(a_records_table)
            self.display_message(f'Found {len(res["dns_records"]["dns"])} A records')
        else:
            res['dns_records']['dns'] = []
            self.display_message('No A records table found')
        
        # Parse MX Records
        if mx_records_table:
            res['dns_records']['mx'] = self.retrieve_mx_records(mx_records_table)
            self.display_message(f'Found {len(res["dns_records"]["mx"])} MX records')
        else:
            res['dns_records']['mx'] = []
            self.display_message('No MX records table found')
        
        # Parse NS Records
        if ns_records_table:
            res['dns_records']['ns'] = self.retrieve_ns_records(ns_records_table)
            self.display_message(f'Found {len(res["dns_records"]["ns"])} NS records')
        else:
            res['dns_records']['ns'] = []
            self.display_message('No NS records table found')
        
        # Parse TXT Records
        if txt_records_table:
            res['dns_records']['txt'] = self.retrieve_txt_record(txt_records_table)
            self.display_message(f'Found {len(res["dns_records"]["txt"])} TXT records')
        else:
            res['dns_records']['txt'] = []
            self.display_message('No TXT records table found')
        
        # For backward compatibility, also store NS records as 'host'
        res['dns_records']['host'] = res['dns_records']['ns']

        # Network mapping image - look for <img> tag with alt="Logo"
        image_data = None
        image_url = None
        try:
            logo_img = soup.find('img', alt='Logo')
            if logo_img and logo_img.get('src'):
                image_url = logo_img.get('src')
                # If it's a relative URL, make it absolute
                if image_url.startswith('/'):
                    image_url = 'https://dnsdumpster.com' + image_url
                elif not image_url.startswith('http'):
                    image_url = 'https://dnsdumpster.com/' + image_url
                
                self.display_message(f'Found image URL: {image_url}')
                image_data = base64.b64encode(self.session.get(image_url).content)
            else:
                # Fallback to old method
                self.display_message('Logo img not found, trying fallback method')
                tmp_url = 'https://dnsdumpster.com/static/map/{}.png'.format(domain)
                image_data = base64.b64encode(self.session.get(tmp_url).content)
                image_url = tmp_url
        except Exception as e:
            self.display_message(f'Error retrieving image: {e}')
            image_data = None
            image_url = None
        finally:
            res['image_data'] = image_data
            res['image_url'] = image_url

        # XLS/XLSX file - look for <a> tag with text "Download xlsx"
        xls_data = None
        xls_url = None
        try:
            # Find the download link
            download_links = soup.find_all('a')
            for link in download_links:
                link_text = link.get_text(strip=True).lower()
                if 'download' in link_text and 'xlsx' in link_text:
                    xls_url = link.get('href')
                    if xls_url:
                        # If it's a relative URL, make it absolute
                        if xls_url.startswith('/'):
                            xls_url = 'https://dnsdumpster.com' + xls_url
                        elif not xls_url.startswith('http'):
                            xls_url = 'https://dnsdumpster.com/' + xls_url
                        
                        self.display_message(f'Found Excel URL: {xls_url}')
                        xls_data = base64.b64encode(self.session.get(xls_url).content)
                        break
            
            # Fallback to pattern matching if the link wasn't found
            if not xls_url:
                self.display_message('Download link not found, trying fallback method')
                pattern = r'/static/xlsx/' + re.escape(domain) + r'-[a-f0-9\-]{36}\.xlsx'
                xls_matches = re.findall(pattern, req.content.decode('utf-8'))
                if xls_matches:
                    xls_url = 'https://dnsdumpster.com' + xls_matches[0]
                    xls_data = base64.b64encode(self.session.get(xls_url).content)
        except Exception as err:
            self.display_message(f'Error retrieving Excel file: {err}')
            xls_data = None
            xls_url = None
        finally:
            res['xls_data'] = xls_data
            res['xls_url'] = xls_url

        return res

