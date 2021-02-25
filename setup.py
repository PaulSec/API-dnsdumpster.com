from setuptools import setup
setup(
  name = 'dnsdumpster',
  packages = ['dnsdumpster'], # this must be the same as the name above
  version = '0.8',
  description = 'DNS Dumpster lib',
  author = 'Paul Sec',
  author_email = 'paulwebsec@gmail.com',
  url = 'https://github.com/PaulSec/API-dnsdumpster.com',
  download_url = 'https://github.com/PaulSec/API-dnsdumpster.com/tarball/0.8',
  keywords = ['dnsdumpster', 'dns', 'harvesting'],
  install_requires=["bs4", "requests"],
  classifiers = [],
)
