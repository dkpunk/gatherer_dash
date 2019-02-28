import requests
import json
import re
import MySQLdb
with open('./input.txt','r') as f:
	i_list=f.readlines()
#print i_list
fileout=open('./output.txt','w+')
fileout.write("Gatherer_IP,Status"+"\n");
conn=MySQLdb.connect('localhost',user='root')
cur=conn.cursor()
out=cur.execute('use gatherer_dashboard')
for element in i_list:
	gip=element.strip()
	out=cur.execute("select distinct(gatherer_ip) from gatherer_vip_mapping where gatherer_ip='{0}'".format(gip))
	datalist=cur.fetchall()
	if(datalist):
		print str(datalist[0])+",Present"
		fileout.write(gip+",Present"+"\n")
	else:
		fileout.write(gip+",NA"+"\n")
conn.close()
fileout.close()
	
	
