from DNSDumpsterAPI import DNSDumpsterAPI

res = DNSDumpsterAPI({'verbose': True}).search('polyconseil.fr')
for entry in res:
	print "%s (%s) %s %s" % (entry['domain'], entry['ip'], entry['as'], entry['provider'])
# print res
