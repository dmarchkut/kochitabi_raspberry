import requests
import json
def post_server(temp):
    data = {
        "environment_id": "en0001",
        "access_point_id": "ap0001",
        "point_temperature": temp,
        "acquisition_rank": 1,
        "created_at": "2018-01-19T01:53:29Z",
        "update_at": "2018-01-19T01:53:31Z",
    }
    r = requests.post("https://ancient-island-44932.herokuapp.com/cms/weather", data = json.dumps(data))
    print(r)
