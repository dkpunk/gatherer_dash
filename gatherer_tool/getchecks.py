#!/usr/local/bin/python
import requests
import time
import json
import re
import datetime
import csv
import sys
import urllib2
#from json2html import *
ip=sys.argv[1]
#environment=sys.argv[2]
environment="Production"
#print(environment)
headers = {"Content-Type":"application/json","Accept":"application/json","charset":"ascii"}
timestr = time.strftime("%Y%m%d")
#tablestr='<table class="table table-bordered style="width:40%" id="example"><caption>Checks present in the Server</caption><thead><tr><th>Server Name</th><th>Current Status</th><th>Check Name</th><th>Command Executed</th><th>interval</th><th>Output</th><th>Last Issued</th><th>last Statuses</th><th>Subscribers</th></tr>i</thead>'
print '''
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
tablestr='<table  id=\"myTable\" class=\"features-table\" style="width:40%" id="example"><caption>Checks present in the Server</caption><thead><tr><th>Server Name</th><th>Current Status</th><th>Check Name</th><th>interval</th><th>Output</th><th>Last Issued</th></tr></thead>'
flag=1
not_running=0
try:
        if(environment=='Production'):
                response = requests.get('http://172.17.54.69:4567/clients',timeout=7)
        #       print(response.text)
                data=json.loads(response.text)
                for element in data:
                        if(element['address']==ip):
#                               print element['name']
                                flag=0
                                response1=requests.get('http://172.17.54.69:4567/results/'+element['name'],timeout=7)
                                data1=json.loads(response1.text)
                                for element1 in data1:
                                        buttondata="NA"
                                        d1=datetime.datetime.fromtimestamp(element1['check']['issued'])
                                        d2=datetime.datetime.fromtimestamp(time.time())
                                        d3=d2-d1
                                        check_issued="{0} || {1} minutes back".format(d1,d3.seconds/60)
                                        if(element1["check"]["status"]==0):
                                                attr="Green"
                                                element1["check"]["status"]="OK"
                                        elif(element1["check"]["status"]==2):
                                                attr="Red"
                                                element1["check"]["status"]="Critical"
                                                buttondata='<a href="resolvecheck.php?call=resolve&hostid='+element['address']+'&checkname='+element1['check']['name']+'" class="btn btn-default" target="_blank">Resolve</a>'
                                        else:
                                                attr="Orange"
                                                element1["check"]["status"]="Warn"
                                        if "interval" in element1["check"]:
                                                pass
                                        else:
                                                element1["check"]["interval"]="NA"
                                        if "command" in element1["check"]:
                                                pass
                                        else:
                                                element1["check"]["command"]="NA"
                                        if "subscribers" in element1["check"]:
                                                pass
                                        else:
                                                element1["check"]["subscribers"]="NA"
                                        if element1["check"]["name"] == 'keepalive':
                                                text = element1["check"]["output"]
                                                m = re.search('for (.+?) seconds', text)
                                                if m:
                                                        found = m.group(1)
                                                        if(found >= 6000):
                                                                not_running=1

                                        #tablestr=tablestr+'<tr class="gradeX"><td>{0}</td><td bgcolor="'.format(element['name'])+attr+'">{1}<td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{6}</td><td>{7}</td><td>{8}</td></tr>'.format(element1['client'],element1['check']['status'],element1['check']['name'],element1['check']['command'].encode('utf-8'),element1['check']['interval'],element1['check']['output'],element1['check']['issued'],element1['check']['history'],element1['check']['subscribers'])
                                        tablestr=tablestr+'<tr class="gradeX"><td>{0}</td><td bgcolor="'.format(element['name'])+attr+'">{1}<td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>'.format(element1['client'],element1['check']['status'],element1['check']['name'],element1['check']['interval'],element1['check']['output'],check_issued)
        elif(environment=='Stage'):
                response = requests.get('http://172.18.38.21:4567/clients',timeout=5)
#               print(response.text)
                data=json.loads(response.text)
                for element in data:
                        if(element['address']==ip):
#                               print element['name']a
                                flag=0
                                response1=requests.get('http://172.18.38.21:4567/results/'+element['name'],timeout=5)
                                data1=json.loads(response1.text)
                                for element1 in data1:
                                        buttondata="NA"
                                        d1=datetime.datetime.fromtimestamp(element1['check']['issued'])
                                        d2=datetime.datetime.fromtimestamp(time.time())
                                        d3=d2-d1
                                        check_issued="{0} || {1} minutes back".format(d1,d3.seconds/60)
                                        if(element1["check"]["status"]==0):
                                                attr="Green"
                                                element1["check"]["status"]="OK"

                                        elif(element1["check"]["status"]==2):
                                                attr="Red"
                                                element1["check"]["status"]="Critical"
                                                buttondata='<a href="resolvecheck.php?call=resolve&hostid='+element['address']+'&checkname='+element1['check']['name']+'" class="btn btn-default" target="_blank">Resolve</a>'
                                        else:
                                                attr="Orange"
                                                element1["check"]["status"]="Warn"
                                        if "interval" in element1["check"]:
                                                pass
                                        else:
                                                element1["check"]["interval"]="NA"
                                        if "command" in element1["check"]:
                                                pass
                                        else:
                                                element1["check"]["command"]="NA"
                                        if "subscribers" in element1["check"]:
                                                pass
                                        else:
                                                element1["check"]["subscribers"]="NA"
                                        if element1["check"]["name"] == 'keepalive':
                                                text = element1["check"]["output"]
                                                m = re.search('for (.+?) seconds', text)
                                                if m:
                                                        found = m.group(1)
                                                        if(found >= 6000):
                                                                not_running=1
                                       # tablestr=tablestr+'<tr class="gradeX"><td>{0}</td><td bgcolor="'+attr+'">{1}<td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{6}</td><td>{7}</td></tr>'.format(element['name'],element1['check']['status'],element1['check']['name'],element1['check']['command'].encode('utf-8'),element1['check']['interval'],element1['check']['output'],d1,buttondata)
                                        tablestr=tablestr+'<tr class="gradeX"><td>{0}</td><td bgcolor="'.format(element['name'])+attr+'">{1}<td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{6}</td></tr>'.format(element1['client'],element1['check']['status'],element1['check']['name'],element1['check']['interval'],element1['check']['output'],check_issued,buttondata)

        tablestr=tablestr+"</table>"
        if(flag==0):
                if(not_running==1):
                        print '<span id="notrunning" class="error">Checks not running since '+found+' seconds,Please check sensu-client</span>';
                print tablestr
        else:
                print "No Checks Available for this Server"
except:
        print "Unable to fetch uchiwa details. Please contact CICD team"
