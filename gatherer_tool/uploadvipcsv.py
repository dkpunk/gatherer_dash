import MySQLdb
import csv
conn=MySQLdb.connect('localhost',user='root')
cur=conn.cursor()
cur.execute('use gatherer_dashboard;')
csvfile=open('./vip_mapping.csv','rb')
reader=csv.reader(csvfile)
count=0
for row in reader:
	if(count==0):
		print "First row"
	else:
		if(row):
			if(row[1] and row[2]):
				print "environment->"+row[0]
				print "vip_and_port->"+row[1]
				print "datacenter->"+row[2]
				out=cur.execute("INSERT IGNORE INTO vip_region_mapping(region,vip_and_port,datacenter) VALUES('"+row[0]+"','"+row[1]+"','"+row[2]+"')")
				print out
	count=count+1
#                                out=cur.execute("INSERT IGNORE INTO vip_environment_mapping(environment,vip_and_port,datacenter) VALUES('"+row[0]+"','"+column+"')")
#                                print row[0]
#                                print "else"
#                                print out
csvfile.close()
conn.commit()
conn.close()
