import requests
import json
import re
import MySQLdb
import datetime
nowtime=datetime.datetime.now()
response=requests.get('http://172.17.54.69:4567/results?filter.check.name=check_sdp2_check_gatherers_process')
print response.status_code
print response.text
file_out=open("/var/www/html/gatherer_tool/gatherer_process_check/allstatus.csv","w+")
if(response.status_code ==200):
	data=json.loads(response.text)
	for element in data:
            print element
	    print element['check']['output']
	    file_out.write(str(element['client'])+","+str(element["check"]["status"])+"\n")
else:
	print "Fetching from sensu Server failed"
file_out.close()
