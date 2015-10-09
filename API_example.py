#!env python
# -*- coding: utf-8 -*-

from DNSDumpsterAPI import DNSDumpsterAPI


res = DNSDumpsterAPI({'verbose': True}).search('microsoft.com')
for entry in res:
	print "%s (%s) %s %s %s" % (entry['domain'], entry['ip'], entry['as'], entry['provider'], entry['country'])
