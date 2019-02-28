import requests
import json
import re
import MySQLdb
import sys
import datetime
import os

os.environ['http_proxy']='http://172.17.25.200:3128'
os.environ['https_proxy']='http://172.17.25.200:3128'
with open('./validation_list') as f:
    for element in f:
	response = requests.get('http://172.17.54.69:4567/clients',timeout=7)
	if(response.status_code!=200):
		critical_network_flag=1
		print element+": Connectivity to uchiwa failed <br>"
        data=json.loads(response.text)
        for element1 in data:
		#print element1['address']
		#print element[0].strip()
        	if(element1['address']==element.strip()):
		###adding subscriber check login######
			response_sub=requests.get('http://172.17.54.69:4567/clients/'+element1['name'])
			data_sub=json.loads(response_sub.text)
			if "sdp2_role_fetch_gatherer" in data_sub['subscriptions']:
                		print element+": Subscription present in Gatherer <br>"
			else:
				print element+": Subscription not present in Gatherer <br>"


