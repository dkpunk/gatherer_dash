import requests
import json
import re
import MySQLdb
import sys
import datetime
vip_port=sys.argv[1]
conn=MySQLdb.connect('localhost',user='root')
cur=conn.cursor()
out=cur.execute('use gatherer_dashboard')
#cur.execute("select distinct(gatherer_ip) from gatherer_vip_mapping where vip_and_port='{0}'".format(vip_port))
#cur.execute("select distinct(gatherer_ip),timestamp from gatherer_vip_mapping where vip_and_port='{0}' and timestamp=(select max(timestamp) from gatherer_vip_mapping where vip_and_port='{0}')".format(vip_port))
cur.execute("select distinct(gatherer_ip),timestamp from gatherer_vip_mapping where vip_and_port='{0}'".format(vip_port))
gatherer_list=cur.fetchall()
cur.execute("select max(timestamp) from gatherer_vip_mapping")
max_date=cur.fetchall()
max_date1=max_date[0][0]
def get_gatherer_thread_count(ip):
	cur.execute("select gatherer_thread_count from gatherer_vip_mapping where gatherer_ip='{0}'".format(ip))
	result=cur.fetchall()
	return result[0][0]
#print max_date1-max_date1
#print datacenter_list
#print region_list
print '''
<!DOCTYPE html>
<html>
<head><title>Gatherer Details</title></head><body>
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
	
print "<h2>Gatherers Details for {0}</h2>".format(vip_port)
print '<input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search for IP" title="Type in a name">'
print "<table id=\"myTable\" class=\"table table-bordered\" style=\"width:100%\">"
print "<thead><tr><th style=\"background:#b4bab6\"><b>Gatherers</b></th><th>Gatherer Status</th><th>Sensu/Gatherer Sync</th><th style=\"background:#b4bab6\"><b>Critical Checks on Sensu</b></th><th>Thread Count</th></thead>"
if len(gatherer_list)==0:
	 print "<tr><td>No Gatherers mapped to this VIP</td><td></td><td></td></tr>"
for element in gatherer_list:
    try:	
	update_flag=1
	more_inf=""
	tmp_date=(max_date1-element[1])
	c_count=0
	critical_check_flag=0
	critical_network_flag=1
	check_names=""
	sub_flag=1
	g_check_flag=1
	gatherer_thread_count=get_gatherer_thread_count(element[0])
	if(tmp_date.seconds==0):
                update_flag=0
                more_inf=more_inf+"Gatherer at Latest Update <br>"
	else:
		more_inf=more_inf+"Gatherer Moved or not Updated since {0}<br>".format(element[1])
	
	response1=requests.get('http://172.17.54.69:4567/results/'+host_ip_dict[element[0]],timeout=7)
        data1=json.loads(response1.text)
	for json_data in data1:
		if(json_data["check"]["status"] == 2):
			critical_check_flag=1
			check_names=check_names+json_data["check"]["name"]+"<br>"
			c_count=c_count+1
		if(json_data['check']['name']== 'check_sdp2_check_gatherers_process' and json_data["check"]["status"] == 0):
			g_check_flag=0
		elif(json_data['check']['name']== 'check_sdp2_check_gatherers_process' and json_data["check"]["status"] == 2):
			g_check_flag=2
			
			
	
	print "<tr><td><a href=\"getchecks.php?ip="+element[0]+"\">"+element[0]+"</a></td>"
	if(g_check_flag==0):
                print "<td>Online &nbsp;&nbsp; <img src=\"./cssjs/greentick.png\" style=\"width:20px; height:20px\" title=\"Online\"></td>"
        elif(g_check_flag==2):
                print "<td>Offline &nbsp;&nbsp; <img src=\"./cssjs/redtick.png\" style=\"width:20px; height:20px\" title=\"Offline\"></td>"
        else:
                print "<td>Sensu Check not running &nbsp;&nbsp; <img src=\"./cssjs/redtick.png\" style=\"width:20px; height:20px\" title=\"Offline\"></td>"
	'''if(critical_network_flag==1):
		print "<td bgcolor=\"#ff471a\">No</td>"
	else:
		print "<td bgcolor=\"#79ff4d\">Yes</td>"

	if(sub_flag==1):
		print "<td bgcolor=\"#ff471a\">No</td>"
	else:
		print "<td bgcolor=\"#79ff4d\">Yes</td>"
	'''
	#print "<td>{1}</td>".format(element[0],element[1],more_inf)
	if(update_flag==1):
                print "<td>No  &nbsp;&nbsp; <img src=\"./cssjs/redtick.png\" style=\"width:20px; height:20px\" title=\"No\"><br>{0}</td>".format(more_inf)
        else:
                print "<td>Yes  &nbsp;&nbsp; <img src=\"./cssjs/greentick.png\" style=\"width:20px; height:20px\" title=\"Yes\"></td>"
	if(critical_check_flag==1):
                #buttondata='<a href="resolvegatherer.php?ip='+element[0]+'&vip_port='+vip_port+' class="btn btn-default" target="_blank">Resolve</a>'
                print "<td>Critical Checks  &nbsp;&nbsp; <img src=\"./cssjs/redtick.png\" style=\"width:20px; height:20px\" title=\"Crtical Checks\">:<br>{2}<a href=\"getchecks.php?ip={0}\"><br>More info</a></td>".format(element[0],c_count,check_names)
        else:
                print "<td>No Critical Alerts on Sensu  &nbsp;&nbsp; <img src=\"./cssjs/greentick.png\" style=\"width:20px; height:20px\" title=\"Offline\"></td>"
	print "<td>{0}</td></tr>".format(gatherer_thread_count)
    except KeyError:
	print "<tr><td><a href=\"getchecks.php?ip={0}\">"+element[0]+"</a></td><td bgcolor=\"#ffb84d\">Sensu Check not running</td><td bgcolor=\"#ff471a\">Unable to get details</td><td>Unable to get details</td><td>Unable to get details</td></tr>"

print "</table>"
print '''<script src="./cssjs/jquery-1.12.4.js"></script>
		     <script src="./cssjs/jquery.dataTables.min.js"></script>
		     <script src="./cssjs/dataTables.bootstrap.min.js"></script>
		      <link href="./cssjs/bootstrap.min.css" rel="stylesheet">
		      <link href="./cssjs/dataTables.bootstrap.min.css" rel="stylesheet">
		    <script>
		$(document).ready(function() {
		     $('#myTable').DataTable({
		"pageLength":60
		});
		    $('#myHeader').append("<a href='http://172.17.15.222/gatherer_tool/getactivegatherer.php' target='_blank'>:     690/753  (Online/Total)</a>");
		} );
		</script></body></html>'''
conn.close()
#print more_inf
	
	
