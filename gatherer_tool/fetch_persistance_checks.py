import requests
import json
import re
my_regex="*"+re.escape("(P)CRITICAL")+"*"
response=requests.get('http://172.17.54.69:4567/events')
role_check_dict={}
file_out=open("/home/asingh7/gatherer_fetch/persistent_Server_list","w")
file_out1=open("/home/asingh7/gatherer_fetch/persistent_csv","w")
print response.status_code
#print response.text
if(response.status_code ==200):
	data=json.loads(response.text)
	for element in data:
		output_data=element["check"]["output"]
#		if(re.search("*(P)CRITICAL*",element["check"]["output"])):
		if(output_data.find('(P)CRITICAL') != -1):
			print element["check"]["output"]
			ip=element["client"]["address"]
			if (ip in role_check_dict.keys() and "instance" in element["check"].keys()):
				role_check_dict[ip].append(element["check"]["instance"])
				file_out1.write("IP:"+ip+",Instance:"+element["check"]["instance"]+"\n")
			elif( "instance" in element["check"].keys()):
				role_check_dict.update({ip :[]})
				role_check_dict[ip].append(element["check"]["instance"])
				file_out1.write("IP:"+ip+",Instance:"+element["check"]["instance"]+"\n")
print json.dumps(role_check_dict,indent=2)
file_out.write(json.dumps(role_check_dict,indent=2))
file_out1.close()
