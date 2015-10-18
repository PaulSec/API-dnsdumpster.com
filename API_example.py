from DNSDumpsterAPI import DNSDumpsterAPI

res = DNSDumpsterAPI(False).search('microsoft.com')
for entry in res:
	print "%s (%s) %s %s %s" % (entry['domain'], entry['ip'], entry['as'], entry['provider'], entry['country'])
