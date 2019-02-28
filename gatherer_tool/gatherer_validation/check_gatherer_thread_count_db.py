import requests
import json
import re
import MySQLdb
#print i_list
fileout=open('./thread_db.txt','w+')
conn=MySQLdb.connect('localhost',user='root')
cur=conn.cursor()
out=cur.execute('use gatherer_dashboard')
out=cur.execute("select distinct(gatherer_ip) from gatherer_vip_mapping where gatherer_thread_count='NA'")
fields=cur.fetchall()
for element in fields:
	fileout.write(element[0]+"\n")
conn.close()
fileout.close()
	
	
