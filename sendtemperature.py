import requests
import json
def post_server(temp):
    data = {
        "coord": {"lon": 20, "lat": 20}, 
        "weather":[{"id": 803, "main": "Clouds"}],
        "main":{"temp": temp, "tempmax":999}, 
        "cod": 200
    }
    r = requests.post("https://pure-tundra-22058.herokuapp.com/cms/temperature", data = json.dumps(data))
    print(r)

