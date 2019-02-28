import requests
import json
import re
import MySQLdb
import datetime
nowtime=datetime.datetime.now()
conn=MySQLdb.connect('localhost',user='root')
cur=conn.cursor()
out=cur.execute('use gatherer_dashboard')
response = requests.get('http://172.17.54.69:4567/clients',timeout=15)
host_ip_dict={}
name_check_dict={}
try:
   if(response.status_code!=200):
        print "<h3>Connectivity to uchiwa failed</h3>"
   else:
        data=json.loads(response.text)
        for element1 in data:
                host_ip_dict[element1['name']]=element1['address']
except Exception as e :
        print(e)
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
response=requests.get('http://172.17.54.69:4567/results?filter.check.name=check_sdp2_check_gatherers_process',headers)
print response.status_code
print response.text
if(response.status_code ==200):
	data=json.loads(response.text)
#	print "Deleting Old Entries"
#	out=cur.execute("delete from gatherer_vip_mapping")
#	print out
	for element in data:
            print element
	    print element['check']['output']
	    print "Client name |"
	    print element['client']
	    client=element['client']
	    gatherer_ip=host_ip_dict[client]
	    gatherer_status="NA"
	    gatherer_thread_count="NA"
	    if element['check']['output']:
		ARR=element['check']['output'].split(":")
		if(len(ARR) >= 3):
		    gatherer_status=ARR[1]
                    gatherer_thread_count=ARR[3]
		    print "Gatherer"+gatherer_ip
    		    print "Gatherer Status"+gatherer_status
		    print "Thread count"+gatherer_thread_count
	    try:
		#outinsert=cur.execute("INSERT INTO gatherer_vip_mapping(gatherer_ip,vip_and_port,timestamp) VALUES(%s,%s,%s) on duplicate key update timestamp=%s",(g_temp,vip_temp,nowtime,nowtime))
		outinsert=cur.execute("UPDATE gatherer_vip_mapping SET gatherer_status='{0}',gatherer_thread_count='{1}',update_flag=1,timestamp='{3}' where gatherer_ip='{2}'".format(gatherer_status,gatherer_thread_count,gatherer_ip,nowtime))
	    except MySQLdb.Error,e:
			print  "Gatherer: "+str(gatherer_ip)+"Exception Found"+str(e)
else:
	print "Fetching from sensu Server failed"
conn.commit()
conn.close()
	
