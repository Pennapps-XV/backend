import json
import sys
import requests

image = sys.argv[1]

def post_some_dict(dict):
    headers = {'Content-type': 'application/json'}
    r = requests.post("http://127.0.0.1:5000/search", data=json.dumps(dict), headers=headers)
    return r.text

print(json.loads(post_some_dict({"image_url": image}))['links'][0])
