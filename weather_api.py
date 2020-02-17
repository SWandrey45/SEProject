import requests
import json
response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Dublin,IE&APPID=2a2021764b2563bfa694c9146727bc6c")
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


jprint(response.json())
