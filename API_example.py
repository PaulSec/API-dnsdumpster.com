from DNSDumpsterAPI import DNSDumpsterAPI

res = DNSDumpsterAPI({'verbose': True}).search('microsoft.com')
print res
