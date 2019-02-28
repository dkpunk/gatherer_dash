import requests
import json
import re
import MySQLdb
response = requests.get('http://172.17.54.69:4567/clients',timeout=7)
host_ip_dict={}
try:
   if(response.status_code!=200):
        print "<h3>Connectivity to uchiwa failed</h3>"
   else:
        data=json.loads(response.text)
        for element1 in data:
                host_ip_dict[element1['address']]=element1['name']
        #print "host_ip_dict"+str(host_ip_dict)
except Exception as e :
        print(e)
        exit()
fileout=open('./check_output.txt','w+')
#fileout.write("Gatherer_IP,Status"+"\n");
conn=MySQLdb.connect('localhost',user='root')
cur=conn.cursor()
out=cur.execute('use gatherer_dashboard')
out=cur.execute("select distinct(gatherer_ip) from gatherer_vip_mapping")
datalist=cur.fetchall()
if(datalist):
    for element in datalist:
	try:
	  g_check_flag=0
	  print element[0]
	  response1=requests.get('http://172.17.54.69:4567/results/'+host_ip_dict[element[0]],timeout=7)
	  if(response1.text):
            data1=json.loads(response1.text)
            for json_data in data1:
		if(json_data['check']['name']== 'check_sdp2_check_gatherers_process' and json_data["check"]["status"] == 0):
                        g_check_flag=1
                elif(json_data['check']['name']== 'check_sdp2_check_gatherers_process' and json_data["check"]["status"] == 2):
                        g_check_flag=2
	    if(g_check_flag==0):
		fileout.write(element[0]+",Failed"+"\n")
	    else:
		fileout.write(element[0]+",Present"+"\n")
	except:
		print "Not Found"+element[0]
conn.close()
fileout.close()
	
		
