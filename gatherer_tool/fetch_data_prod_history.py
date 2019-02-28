import requests
import json
import re
import MySQLdb
conn=MySQLdb.connect('localhost',user='root')
cur=conn.cursor()
out=cur.execute('use gatherer_dashboard')


response=requests.get('http://172.17.54.69:4567/results?filter.check.name=check_sdp2_fetch_gatherers_vip')
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
		ARR=element['check']['output'].split("-")
		ARR2=ARR[1].split('=')
		print "Gatherer"+ARR2[0]
		ARR3=ARR2[1].split(',')
		for gelement in ARR3:
			#print "Gatherer->"+ARR2[0]
			g_temp=ARR2[0].strip()
			vip_temp=gelement.strip()
			print "Gatherer->"+g_temp
			print "VIP->"+vip_temp
			if(gelement):
	#	only insert		outinsert=cur.execute("INSERT IGNORE INTO gatherer_vip_mapping(gatherer_ip,vip_and_port,timestamp) VALUES('"+ARR2[0]+"','"+gelement+"',NOW())")
				outinsert=cur.execute("INSERT INTO gatherer_vip_mapping_history(gatherer_ip,vip_and_port,timestamp) VALUES('"+g_temp+"','"+vip_temp+"',NOW())")
				print outinsert
else:
	print "Fetching from sensu Server failed"
conn.commit()
conn.close()

	
