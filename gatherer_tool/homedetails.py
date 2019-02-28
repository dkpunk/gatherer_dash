import requests
import json
import re
import MySQLdb
import csv
conn=MySQLdb.connect('localhost',user='root')
cur=conn.cursor()
out=cur.execute('use gatherer_dashboard')
out=cur.execute("select distinct(datacenter) from vip_region_mapping")
datacenter_list=cur.fetchall()
#print datacenter_list
out=cur.execute("select distinct(region) from vip_region_mapping")
region_list=cur.fetchall()
#print region_list
response = requests.get('http://172.17.54.69:4567/clients',timeout=7)
host_ip_dict={}
name_check_dict={}
with open('./gatherer_process_check/allstatus.csv','rb') as csvfile:
        csvreader=csv.reader(csvfile,delimiter=',')
        for row in csvreader:
                name_check_dict[row[0]]=row[1]
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
def getstatus(servername):
   try:
	server_host=host_ip_dict[servername].strip()
	#print server_host
	if(name_check_dict[server_host]=='0'):
		return 0
	else:
		return 1
   except:
	return 1
print '''
<!DOCTYPE html>
<html>
<head>
<style>
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
  border-radius: 5px;
}

/*Body*/
.features-table tbody td {
  text-align: center;
  font: normal 12px Verdana, Arial, Helvetica;
  width: 150px;
}
.features-table td:nth-child(1) {
  font: bold 12px 'trebuchet MS', 'Lucida Sans', Arial;
//  background: #928DB3;
  background : #5380db
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
print "<h2>Gatherers Details</h2>"
print '<input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search for region names.." title="Type in a name">'
print "<table id=\"myTable\" class=\"features-table\" style=\"width:100%\">"
print "<thead><tr><th style=\"background:#b4bab6\"><b>Region\Datacenter</b></th>"
headcount=len(datacenter_list)
for element in datacenter_list:
	print "<th>{0}</th>".format(element[0])
print "</tr></thead>"
for relement in region_list:
	print "<tr><td>{0}</td>".format(relement[0])
	for num in range(headcount):
		#print "<td>{0} {1}</td>".format(datacenter_list[num][0],relement[0])		
		print "<td>"
		curtab=conn.cursor()
		out=curtab.execute("select distinct(vip_and_port) from vip_region_mapping where datacenter='{0}' and region='{1}'".format(datacenter_list[num][0],relement[0]))
		vip_list=curtab.fetchall()
		curtab.close()
		for vip_elem in vip_list:
			print "VIP : <a href=\"fetchgathererbyvip.php?vip_port={0}\">{0}</a>".format(vip_elem[0])
			curtab=conn.cursor()
			curtab.execute("select count(distinct(gatherer_ip)) from gatherer_vip_mapping where vip_and_port='{0}'".format(vip_elem[0]))
			gatherer_count=curtab.fetchall()
			curtab.execute("select distinct(gatherer_ip) from gatherer_vip_mapping where vip_and_port='{0}'".format(vip_elem[0]))
			gatherers_list=curtab.fetchall()
			curtab.close()
			for gatherer_elem in gatherer_count:
				if(gatherer_elem[0] and vip_elem[0]):
					scount=0
					fcount=0
					for servername in gatherers_list:
						server_temp=servername[0]
						server_status=getstatus(server_temp)
#						print servername[0]+"status"+server_status+":"
					    	if(server_status==0):
							scount=scount+1
						else:
							fcount=fcount+1
					
					print "<br>Gatherer count {1}/{0}<br> {1} gatherers online <br> {2} gatherers offline".format(int(gatherer_elem[0]),scount,fcount)
				else:
					print "<br>Gatherer count : NA<br>"
	print "</td></tr>"
print "</table>"
print '''<script>
function myFunction() {
  // Declare variables 
  var input, filter, table, tr, td, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    } 
  }
}
</script>'''
conn.close()
	
	
