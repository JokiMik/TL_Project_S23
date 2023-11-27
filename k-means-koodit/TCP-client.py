# echo-client.py
#pip install requests

import requests


url = "http://172.20.241.9/luedataa_kannasta_groupid_csv.php?groupid=5"  

response = requests.get(url)

print(response.text)

with open('data.csv', 'w') as file:
    file.write(response.text)

