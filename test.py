import score
import shutil
from urllib.request import urlopen
from IPython.display import Image, HTML, display
import requests
import json
import numpy as np
from base64 import b64encode

image_uri = 'http://jp8.r0tt.com/l_89cce6d0-f032-11e1-8ac2-33f655e00008.jpg'
service_uri = 'http://104.211.38.248:80/score'

with urlopen(image_uri) as response:
    with open('temp.jpg', 'bw+') as f:
        shutil.copyfileobj(response, f)

def image_to_json(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    base64_bytes = b64encode(content)
    base64_string = base64_bytes.decode('utf-8')
    raw_data = {'image': base64_string}
    return json.dumps(raw_data, indent=2)

# Turn image into json and send an HTTP request to the prediction web service
input_data = image_to_json('temp.jpg')
headers = {'Content-Type':'application/json'}
resp = requests.post(service_uri, input_data, headers=headers)

# Extract predication results from the HTTP response
result = resp.text.strip("}\"").split("[")
predications = result[1].split(",")
print ("Predication results:")
for temp in predications:
    print (temp.strip("]").replace('\\','').strip().strip("\"").strip("}"))
Image('temp.jpg')