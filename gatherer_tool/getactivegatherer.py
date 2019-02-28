import requests
import json
import re
import MySQLdb
import sys
import datetime
conn=MySQLdb.connect('localhost',user='root')
cur=conn.cursor()
out=cur.execute('use gatherer_dashboard')
import csv
#cur.execute("select distinct(gatherer_ip) from gatherer_vip_mapping where vip_and_port='{0}'".format(vip_port))
cur.execute("select distinct(gatherer_ip),vip_and_port,gatherer_status,gatherer_thread_count,timestamp,update_flag from gatherer_vip_mapping;")
gatherer_list=cur.fetchall()
cur.execute("select count(distinct(gatherer_ip)) from gatherer_vip_mapping;")
out_list=cur.fetchall()
gatherer_total_count=int(out_list[0][0])
cur.execute("select count(distinct(gatherer_ip)) from gatherer_vip_mapping where gatherer_status = 'NA' or gatherer_status = NULL or update_flag=0")
out_list=cur.fetchall()
gatherer_failed_count=int(out_list[0][0])
gatherer_success_count=gatherer_total_count-gatherer_failed_count
#print datacenter_list
#print region_list
'''
response = requests.get('http://172.17.54.69:4567/clients',timeout=7)
host_ip_dict={}
name_check_dict={}
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
with open('./gatherer_process_check/allstatus.csv','rb') as csvfile:
	csvreader=csv.reader(csvfile,delimiter=',')
	for row in csvreader:
		name_check_dict[row[0]]=row[1]
		
'''				
		
print '''
<!DOCTYPE html>
<html>
<head><title> All Gatherer Details</title></head><body>
'''
'''<style>
#myInput {
    background-position: 10px 12px; /* Position the search icon */
    background-repeat: no-repeat; /* Do not repeat the icon image */
    width: 100%; /* Full-width */
    font-size: 16px; /* Increase font-size */
    padding: 12px 20px 12px 40px; /* Add some padding */
    border: 1px solid #ddd; /* Add a grey border */
    margin-bottom: 12px; /* Add some space below the input */
}

.features-table {
  width: 100%;
  margin: 0 auto;
  border-collapse: separate;
  border-spacing: 0;
  color: #2a2a2a;
t background: #fafafa;  
  background-image: linear-gradient(top, #fff, #eaeaea, #fff);
}

.features-table td {
  height: 50px;
  line-height: 50px;
  padding: 0 20px;
  border-bottom: 1px solid #cdcdcd;
  box-shadow: 0 1px 0 white;
  white-space: nowrap;
  text-align: center;
  border: 1px solid grey;
  border-radius: 10px;
}

/*Body*/
.features-table tbody td {
  text-align: center;
  font: normal 12px Verdana, Arial, Helvetica;
  width: 150px;
}


.features-table tbody td:first-child {
  width: auto;
  text-align: left;
}


/*Header*/
.features-table thead th{
  height: 50px;
  line-height: 50px;
  padding: 0 20px;
  border-bottom: 1px solid #cdcdcd;
  box-shadow: 0 1px 0 white;
  white-space: nowrap;
  text-align: center;
  font: bold 12px 'trebuchet MS', 'Lucida Sans', Arial;
  //background: #CBDA29;
  background:#e0dd1a
}

/*Footer*/
.features-table tfoot td {
  font: bold 1.4em Georgia;  
  border-radius-bottomright: 10px;
  border-radius-bottomleft: 10px; 
  border-bottom-right-radius: 10px;
  border-bottom-left-radius: 10px;
  border-bottom: 1px solid #dadada;
}

.features-table tfoot td:first-child {
  border-bottom: none;
}
</style>'''
print "<h2 id=\"myHeader\">ALL ACTIVE GATHERERS</h2>"
print "<table id=\"myTable\" class=\"table table-bordered\" style=\"width:100%\">"
print "<thead><tr><th style=\"background:#b4bab6\"><b>Gatherers</b></th><th style=\"background:#b4bab6\"><b>VIP Mapped</b></th><th style=\"background:#b4bab6\"><b>Gatherer Process Status</b></th><th style=\"background:#b4bab6\"><b>Gatherer Thread Count</b></th><th style=\"background:#b4bab6\"><b>Last Checked</b></th><th style=\"background:#b4bab6\"><b>Updated</b></th></tr></thead>"
if len(gatherer_list)==0:
	 print "<tr><td>No Gatherers mapped to this VIP</td><td></td><td></td></tr>"
file_out=open("./gatherer_conf_missing_list","w+")
for element in gatherer_list:
	'''
	if element[0] in host_ip_dict.keys():
		tmp_host_name=host_ip_dict[element[0]]
		#print name_check_dict[tmp_host_name]
		if(tmp_host_name in name_check_dict.keys()):
		    if(name_check_dict[tmp_host_name].strip()=='0'):
			print "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td bgcolor=\"green\">Process Up</td></tr>".format(element[0],element[1],element[2])
		    elif(name_check_dict[tmp_host_name].strip()=='2'):
			print "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td bgcolor=\"red\">Process Down</td></tr>".format(element[0],element[1],element[2])
		    else:
			print "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td bgcolor=\"orange\">Check Failed</td></tr>".format(element[0],element[1],element[2])
			file_out.write("{0},Check Failed\n".format(element[0]))
		else:
		    print "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td bgcolor=\"orange\">Check Failed</td></tr>".format(element[0],element[1],element[2])
		    file_out.write("{0},Check Failed\n".format(element[0]))
	else:
		print "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td bgcolor=\"red\">NA</td></tr>".format(element[0],element[1],element[2])
  		file_out.write("{0},Check Failed\n".format(element[0]))
	'''
	print "<tr><td>{0}</td><td>{1}</td>".format(element[0],element[1])
	if(element[2] is not None):
	    if("Gatherer process up" in element[2]):
                print "<td>{0} &nbsp;&nbsp; <img src=\"./cssjs/greentick.png\" style=\"width:20px; height:20px\" title=\"Online\"></td>".format(element[2])
            else:
                print "<td>{0} &nbsp;&nbsp; <img src=\"./cssjs/redtick.png\" style=\"width:20px; height:20px\" title=\"Offline\"></td>".format(element[2])
	else:
	    	 print "<td>NA &nbsp;&nbsp; <img src=\"./cssjs/redtick.png\" style=\"width:20px; height:20px\" title=\"Offline\"></td>".format(element[2])
	if(element[3] is not None):
    	    if(element[3].strip()=="NA"):
                print "<td>{0} &nbsp;&nbsp; <img src=\"./cssjs/redtick.png\" style=\"width:20px; height:20px\" title=\"Gatherer not updated.Please run cookbook\"></td>".format(element[3])
            else:
                print "<td>{0} &nbsp;&nbsp; <img src=\"./cssjs/greentick.png\" style=\"width:20px; height:20px\" title=\"{0}\"></td>".format(element[3])
	else:
	    print "<td>NA &nbsp;&nbsp; <img src=\"./cssjs/redtick.png\" style=\"width:20px; height:20px\" title=\"Gatherer not updated.Please run cookbook\"></td>".format(element[3])
	print "<td>{0}</td>".format(element[4])	
	if(element[5]==1):
	    print "<td>yes &nbsp;&nbsp; <img src=\"./cssjs/greentick.png\" style=\"width:20px; height:20px\"></td>"
	else:
	    print "<td>no &nbsp;&nbsp; <img src=\"./cssjs/redtick.png\" style=\"width:20px; height:20px\"></td>"
				
	print "</tr>"
print "</table>"
print '''
<script src="./cssjs/jquery-1.12.4.js"></script>
     <script src="./cssjs/jquery.dataTables.min.js"></script>
     <script src="./cssjs/dataTables.bootstrap.min.js"></script>
      <link href="./cssjs/bootstrap.min.css" rel="stylesheet">
      <link href="./cssjs/dataTables.bootstrap.min.css" rel="stylesheet">
    <script>
$(document).ready(function() {
     $('#myTable').DataTable({
"pageLength":300
});
     $('#myHeader').append("   <div style='text-align:right'>          Total:'''+str(gatherer_total_count)+''' <br> <img src='./cssjs/greentick.png' style='width:20px; height:20px'> &nbsp;&nbsp; Online:'''+str(gatherer_success_count)+''' <br> <img src='./cssjs/redtick.png' style='width:20px; height:20px'> &nbsp;&nbsp; Offline/NA:'''+str(gatherer_failed_count)+''' </div> ");
} );


</script>
'''
	
	
