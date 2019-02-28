import requests
import json
import re
import MySQLdb
import sys
import os
import csv
#import checkgatherercount
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
except Exception as e :
        print(e)
dc_name=sys.argv[1]
dc_list={"UK_Cloud":("ACC_TECH_UK","HSBC_UK","ING_UK","UK-YI-RESTMASTER","Yichannel_UK"),"US-SC9":("ALLY_CG16","AMEX_PAYPAL","BANVCHE_CG16","BOFA","CASTLIGHT","CG2","CHANNEL_CG11","CHASE","CITI","DEVELOPER-YOSHI2","DEVELOPER_YOSHI","ENVESTNET","FIDELITY","GOOGLE","INTERNATIONAL_CG9","LARGE_BACKEND_CG8","Morgan_stanley","PaypalCobrandGroup","PROD_YOSHI","SDKEE","SDP3_YISTAC","SDP3_yodcredit","YIChannel","YI_COBRAND","YODLEE","YOD_DEM0_SITE"),"SLAU_Cloud": ("Qsuper-AUYI",),"SLCA_Cloud":("CA-YOSHI","CANADA_FI","CENTRAL_ONE_CANADA","RBC_CANNADA"),"IDC":("IDC","IDC-Firemem_us","IDCYIRESTMASTER","IN-YOSHI-PROD","India-ABMU")}
g_total=0
g_pass=0
region_list=dc_list[dc_name]
def check_status(cob_name,limit):
        stdin,stdout=os.popen2("cat /var/www/html/gatherer_tool/cobrand_threshold | grep "+cob_name+": | cut -d':' -f2")
        stdin.close()
        output=stdout.readlines();stdout.close()
        #print "output"+str(output[0])
	try:
            if(output[0]):
                if(int(limit) < int(output[0])):
                        return 1,output[0]
                else:
                        return 0,output[0]
            else:
                return 1,0
	except IndexError:
		return 1,0
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
conn=MySQLdb.connect('localhost',user='root')
cur=conn.cursor()
out=cur.execute('use gatherer_dashboard')
print '''
<!DOCTYPE html>
<html>
<head><title> Gatherer Dashboard</title><body>
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
  border-radius: 5px;
}

/*Body*/
.features-table tbody td {
  text-align: center;
  font: normal 12px Verdana, Arial, Helvetica;
//  width: 150px;
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
print "<h2 id=\"myHeader\">Gatherers Details for "+dc_name+"</h2>"
print '<input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search for region names.." title="Type in a name">'
print "<table id=\"myTable\" class=\"table table-bordered\" style=\"width:100%\">"
#print "<thead><tr><th style=\"background:#b4bab6\"><b>Cobrand Group\Region</b></th>"
print "<thead><tr><th><b>Cobrand Group</b></th><th><b>VIP Assigned</b></th><th><b>Gatherers Configured</b></th><th><b>Gatherers Online</b></th><th><b>Gatherers Offline</b></th>"
#print "<th>{0}</th>".format(dc_name)
#print "<th>Gatherer Count</th>"
print "</tr></thead><tbody>"
for relement in region_list:
			#print "<tr><td>{0}</td>".format(relement)
			#print "<td>{0} {1}</td>".format(datacenter_list[num][0],relement[0])	
			#print "<td>"	
			curtab=conn.cursor()
			out=curtab.execute("select distinct(vip_and_port) from vip_region_mapping where datacenter='{0}' and region='{1}'".format(dc_name,relement))
			vip_list=curtab.fetchall()
			curtab.close()
			total_count=0
			'''for vip_elem in vip_list:
				print "VIP : <a href=\"fetchgathererbyvip.php?vip_port={0}\">{0}</a>".format(vip_elem[0])
				curtab=conn.cursor()
				curtab.execute("select count(distinct(gatherer_ip)) from gatherer_vip_mapping where vip_and_port='{0}'".format(vip_elem[0]))
				gatherer_count=curtab.fetchall()
				curtab.close()
				for gatherer_elem in gatherer_count:
					if(gatherer_elem[0] and vip_elem[0]):
						print "<br>Gatherer count {1}<br>".format(vip_elem[0],int(gatherer_elem[0]))
						total_count=total_count+int(gatherer_elem[0])
					else:
						print "<br>Gatherer count : NA<br>"'''
			for vip_elem in vip_list:
					print "<tr><td>{0}</td>".format(relement)
					print "<td>VIP : <a href=\"fetchgathererbyvip.php?vip_port={0}\">{0}</a></td>".format(vip_elem[0])
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
							tcount=0
							for servername in gatherers_list:
								server_temp=servername[0]
								server_status=getstatus(server_temp)
		#                                               print servername[0]+"status"+server_status+":"
								if(server_status==0):
									scount=scount+1
								else:
									fcount=fcount+1

							#print "<br>Gatherer count {1}/{0}<br> {1} gatherers online <br> {2} gatherers offline".format(int(gatherer_elem[0]),scount,fcount)
							print "<td>{0}</td><td>{1}&nbsp;&nbsp;<a style='color:white' target=\"_blank\"  href=\"fetchgathererbyvip.php?vip_port={3}&state=online\"><img src=\"./cssjs/greentick.png\" style=\"width:20px; height:20px\" title=\"Gatherers Online\"></a></td><td>{2} &nbsp;&nbsp;<a style='color:white' target=\"_blank\"  href=\"fetchgathererbyvip_online.php?vip_port={3}&state=offline\"><img src=\"./cssjs/redtick.png\" style=\"width:20px; height:20px\" title=\"Gatherers Offline\"></a></td>".format(int(gatherer_elem[0]),scount,fcount,vip_elem[0])
							g_total=g_total+int(gatherer_elem[0])
							g_pass=g_pass+scount
						else:
							print "<td>Gatherer count : NA</td><td></td><td></td>"
						print "</tr>"
			(r_status,thres_count)=check_status(relement,gatherer_elem[0])
total_str=":     {0}/{1}  (Online/Total)".format(g_pass,g_total)
#print "{0}/{1}".format(g_pass,g_total)
print "</tbody></table>"
print '''<script src="./cssjs/jquery-1.12.4.js"></script>
		     <script src="./cssjs/jquery.dataTables.min.js"></script>
		     <script src="./cssjs/dataTables.bootstrap.min.js"></script>
		      <link href="./cssjs/bootstrap.min.css" rel="stylesheet">
		      <link href="./cssjs/dataTables.bootstrap.min.css" rel="stylesheet">
		    <script>
		$(document).ready(function() {
		     $('#myTable').DataTable({
		"pageLength":20
		});
		    $('#myHeader').append("<a href='http://172.17.15.222/gatherer_tool/getactivegatherer.php' target='_blank'>'''+total_str+'''</a>");
		} );
		</script></body></html>'''

conn.close()
			
			
