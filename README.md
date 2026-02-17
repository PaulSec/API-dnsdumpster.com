# DNSDumpster API (UNOFFICIAL)

[![Tests](https://github.com/PaulSec/API-dnsdumpster.com/workflows/tests/badge.svg)](https://github.com/PaulSec/API-dnsdumpster.com/actions)
[![PyPI version](https://badge.fury.io/py/dnsdumpster.svg)](https://pypi.org/project/dnsdumpster/)
[![Python Versions](https://img.shields.io/pypi/pyversions/dnsdumpster.svg)](https://pypi.org/project/dnsdumpster/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> ⚠️ **IMPORTANT DISCLAIMER**: This is an **UNOFFICIAL** API wrapper for dnsdumpster.com that scrapes the public website. 
> 
> **DNSDumpster.com offers an official API plan** for commercial and heavy usage. If you need reliable, production-grade access, please consider their official API: https://dnsdumpster.com/
>
> This unofficial wrapper should be used responsibly and in accordance with DNSDumpster's terms of service.

## Overview

A Python client library for interacting with dnsdumpster.com to retrieve DNS records and subdomain information. This tool is useful for security researchers, penetration testers, and network administrators for reconnaissance purposes.

### Features

- 🔍 Retrieve A, MX, NS, and TXT records for a domain
- 🌐 Extract subdomain information
- 🗺️ Download network mapping images
- 📊 Export results to Excel format
- 🎯 Clean, type-hinted API
- ✅ Comprehensive test coverage
- 📝 Full backward compatibility

## Installation

### From PyPI (Recommended)

```bash
pip install dnsdumpster
```

### From GitHub

```bash
pip install git+https://github.com/PaulSec/API-dnsdumpster.com.git
```

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/PaulSec/API-dnsdumpster.com
cd API-dnsdumpster.com

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

##  Quick Start

```python
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI

# Initialize the API
api = DNSDumpsterAPI(verbose=True)

# Search for a domain
results = api.search('example.com')

# Access the results
print(f"Domain: {results['domain']}")
print(f"DNS Records: {results['dns_records']['dns']}")
print(f"MX Records: {results['dns_records']['mx']}")
print(f"NS Records: {results['dns_records']['ns']}")
print(f"TXT Records: {results['dns_records']['txt']}")
```

## Usage Examples

### Basic Domain Lookup

```python
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI

api = DNSDumpsterAPI()
results = api.search('microsoft.com')

# Print all A records (subdomains)
for record in results['dns_records']['dns']:
    print(f"{record['host']} - {record['ip']} - {record['country']}")
```

### Save Network Map Image

```python
import base64

results = api.search('example.com')

if results['image_data']:
    with open('network_map.png', 'wb') as f:
        f.write(base64.b64decode(results['image_data']))
    print(f"Network map saved! URL: {results['image_url']}")
```

### Export to Excel

```python
import base64

results = api.search('example.com')

if results['xls_data']:
    with open('results.xlsx', 'wb') as f:
        f.write(base64.b64decode(results['xls_data']))
    print("Excel file saved!")
```

### Using Custom Session

```python
import requests
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI

# Create custom session with proxy
session = requests.Session()
session.proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080',
}

api = DNSDumpsterAPI(session=session)
results = api.search('example.com')
```

### Error Handling

```python
from dnsdumpster.DNSDumpsterAPI import (
    DNSDumpsterAPI,
    DNSDumpsterAPIError,
    DNSDumpsterRequestError,
    DNSDumpsterParseError
)

api = DNSDumpsterAPI()

try:
    results = api.search('example.com')
except DNSDumpsterRequestError as e:
    print(f"Network error: {e}")
except DNSDumpsterParseError as e:
    print(f"Parsing error: {e}")
except DNSDumpsterAPIError as e:
    print(f"API error: {e}")
```

## API Response Structure

The `search()` method returns a dictionary with the following structure:

```python
{
    'domain': 'example.com',
    'dns_records': {
        'dns': [  # A Records (subdomains)
            {
                'host': 'subdomain.example.com',
                'ip': '192.0.2.1',
                'reverse_dns': 'reverse.dns.com',
                'asn': 'ASN:12345',
                'asn_name': 'Provider Name',
                'country': 'United States',
                'subnet': '192.0.2.0/24',
                'open_services': '80, 443',
                # Backward compatibility keys:
                'domain': 'subdomain.example.com',
                'as': 'ASN:12345',
                'provider': 'Provider Name'
            }
        ],
        'mx': [  # MX Records
            {
                'priority': '10',
                'server': 'mail.example.com',
                'ip': '198.51.100.1',
                'reverse_dns': 'mail.reverse.com',
                'asn': 'ASN:23456',
                'asn_name': 'Mail Provider',
                'country': 'Germany',
                'subnet': '198.51.100.0/24'
            }
        ],
        'ns': [  # NS Records
            {
                'nameserver': 'ns1.example.com',
                'ip': '203.0.113.1',
                'reverse_dns': 'ns1.reverse.com',
                'asn': 'ASN:34567',
                'asn_name': 'DNS Provider',
                'country': 'United Kingdom',
                'subnet': '203.0.113.0/24'
            }
        ],
        'txt': [  # TXT Records
            'v=spf1 include:_spf.example.com ~all',
            'google-site-verification=abcdef123456'
        ],
        'host': []  # Alias for NS records (backward compatibility)
    },
    'image_data': b'base64_encoded_image_bytes',  # or None
    'image_url': 'https://dnsdumpster.com/static/map/example.com.png',
    'xls_data': b'base64_encoded_excel_bytes',  # or None
    'xls_url': 'https://dnsdumpster.com/static/xlsx/example-uuid.xlsx'
}
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/PaulSec/API-dnsdumpster.com
cd API-dnsdumpster.com

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=dnsdumpster --cov-report=html

# Run specific test file
pytest tests/test_parsing.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_parsing.py::TestRetrieveResults::test_retrieve_results_basic
```

### Code Quality

```bash
# Format code with black
black dnsdumpster/ tests/

# Sort imports
isort dnsdumpster/ tests/

# Lint with flake8
flake8 dnsdumpster/ tests/

# Type checking with mypy
mypy dnsdumpster/

# Run all quality checks
black dnsdumpster/ tests/ && isort dnsdumpster/ tests/ && flake8 dnsdumpster/ tests/ && mypy dnsdumpster/
```

### Project Structure

```
API-dnsdumpster.com/
├── dnsdumpster/              # Main package
│   ├── __init__.py
│   ├── DNSDumpsterAPI.py    # Main API class
│   ├── API_example.py       # Usage example
│   └── requirements.txt
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_parsing.py      # Unit tests
│   └── test_integration.py  # Integration tests
├── .github/
│   └── workflows/           # CI/CD workflows
│       ├── tests.yml
│       └── publish.yml
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── setup.py                 # Package configuration
├── README.md
└── LICENSE
```

## Contributing

We welcome contributions! Here's how you can help:

### Reporting Issues

- Use GitHub Issues to report bugs
- Include Python version, OS, and error messages
- Provide minimal reproducible examples

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Run code quality checks (`black`, `flake8`, `mypy`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Coding Guidelines

- Follow PEP 8 style guide
- Add type hints to all functions
- Write docstrings for public methods
- Maintain backward compatibility
- Keep test coverage above 80%
- Update documentation for new features

## Testing Instructions

### Unit Tests

Test individual parsing methods without network calls:

```bash
pytest tests/test_parsing.py -v
```

### Integration Tests

Test the full API workflow with mocked HTTP responses:

```bash
pytest tests/test_integration.py -v
```

### Coverage Report

```bash
pytest --cov=dnsdumpster --cov-report=term-missing
```

## CI/CD

The project uses GitHub Actions for:

- **Testing**: Runs on every push and PR across Python 3.8, 3.9, 3.10, 3.11, 3.12
- **Linting**: Code quality checks with flake8 and mypy
- **Publishing**: Automatic PyPI deployment on tagged releases

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is an unofficial tool and is not affiliated with or endorsed by dnsdumpster.com. Use responsibly and in accordance with the target website's terms of service and robots.txt. The authors are not responsible for misuse of this tool.

## Support

- 📧 For bugs and feature requests, use [GitHub Issues](https://github.com/PaulSec/API-dnsdumpster.com/issues)
- 💬 For general questions, start a [GitHub Discussion](https://github.com/PaulSec/API-dnsdumpster.com/discussions)
- 🐦 Follow the author on Twitter: [@PaulWebSec](https://twitter.com/PaulWebSec)

## Changelog

### Version 0.10 (Current)
- Complete code refactoring with type hints
- Improved error handling with custom exceptions
- Comprehensive test suite with pytest
- Better documentation and examples
- CI/CD with GitHub Actions
- Full backward compatibility maintained

### Previous Versions
See [CHANGELOG.md](CHANGELOG.md) for full version history.

## Acknowledgments

- Original author: [PaulSec](https://github.com/PaulSec)
- Contributors: See [CONTRIBUTORS.md](https://github.com/PaulSec/API-dnsdumpster.com/graphs/contributors)
- DNSDumpster.com for providing the service

