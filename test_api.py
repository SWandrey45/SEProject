import requests
import json
response = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=eb2ccb1179e38c5251aac92c5182497cd4e7222d")
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


jprint(response.json())
#

