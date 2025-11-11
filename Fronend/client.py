import requests
from requests.auth import HTTPBasicAuth 
value =str(56)
header = {"head":"hello this is client"}
authentication = HTTPBasicAuth("username","Nandhiraja")
params = {"name ":"Nandhi"}
response_post = requests.post("http://127.0.0.1:8000/client/user-data")

# response_post =  requests.get(f"http://127.0.0.1:8000/user/nandhi/{value}",headers=header ,auth=authentication)


print(response_post.headers)
print(response_post)