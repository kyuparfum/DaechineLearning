import requests
import base64
import json
from my_settings import SPOTYPY_KEY

# Step 1 - Authorization
url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

# Encode as Base64
message = f"6d378cc769724ee49b8e6670274bb658:ebe47f0756ee4de7a18a8a1170b73307"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')


headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)

responseObject = r.json()
print(json.dumps(responseObject, indent=2))
