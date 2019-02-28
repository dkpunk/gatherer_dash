import os
import re
import sys
cob_name=sys.argv[1]
limit=sys.argv[2]

def check_status(cob_name,limit):
	stdin,stdout=os.popen2("cat /var/www/html/gatherer_tool/cobrand_threshold | grep "+cob_name+" | cut -d':' -f2")
	stdin.close()
	output=stdout.readlines();stdout.close()
	#print "output"+str(output[0])
	if(output[0]):
		if(limit < output[0]):
			return 1
		else:
			return 0
	else:
		return 1

print "Cobrand status"+str(check_status(cob_name,limit))
