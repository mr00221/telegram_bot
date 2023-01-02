import requests

URL = 'http://localhost:8000/app1/users/'
jsondata = {"userID": 123, "veljavnost": "2022-02-02", "ime": "Ime test", "opis": "Opis test"}
r = requests.post(url=URL, json=jsondata)

data = r.json()

print(data)