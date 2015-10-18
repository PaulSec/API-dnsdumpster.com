#!env python
# -*- coding: utf-8 -*-

from DNSDumpsterAPI import DNSDumpsterAPI

res = DNSDumpsterAPI(False).search('microsoft.com')
for entry in res:
    print("{domain} ({ip}) {as} {provider} {country}".format(**entry))
