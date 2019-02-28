import requests
import json
import re
import MySQLdb
import sys
gatherer_list=sys.argv[1].split(",")
vip=sys.argv[2]
conn=MySQLdb.connect('localhost',user='root')
cur=conn.cursor()
out=cur.execute('use gatherer_dashboard')

for g_ip in gatherer_list:
	aa=re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",g_ip)	
	if(aa):	
		#print g_ip+" "+vip
		cur.execute("select * from gatherer_vip_mapping where gatherer_ip='"+g_ip+"' and vip_and_port='"+vip+"'")
		output=cur.fetchall()
		print "Deleted"+str(output)
	else:
		print "Invalid IP"+g_ip

#	outinsert=cur.execute("DELETE FROM gatherer_vip_mapping where gatherer_ip='"+g_ip+"' and vip_and_port='"+vip+"'")
conn.commit()
conn.close()

	
