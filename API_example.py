#!env python
# -*- coding: utf-8 -*-

from DNSDumpsterAPI import DNSDumpsterAPI
import json

res = DNSDumpsterAPI(True).search('microsoft.com')

print "####### Domain #######"
print res['domain']

print "\n\n\n####### DNS Servers #######"
for entry in res['dns_records']['dns']:
    print("{domain} ({ip}) {as} {provider} {country}".format(**entry))

print "\n\n\n####### MX Records #######"
for entry in res['dns_records']['mx']:
    print("{domain} ({ip}) {as} {provider} {country}".format(**entry))

print "\n\n\n####### Host Records (A) #######"
for entry in res['dns_records']['host']:
    print("{domain} ({ip}) {as} {provider} {country}".format(**entry))

print "\n\n\n####### TXT Records #######"
for entry in res['dns_records']['txt']:
	print entry
