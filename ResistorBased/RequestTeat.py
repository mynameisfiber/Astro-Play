import requests
payload = {'0':'f','1':'10'}
r = requests.get("http://10.2.108.1:9999",params=payload)


#r= requests.post("http://10.2.108.1:9999", data  = "{'cmd1':'f 10'}")
