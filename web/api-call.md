
# Calling a REST API

```python
import httplib2
import json
from urllib import urlencode

def getGeocodeLocation(address):
    endpoint_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    google_api_key = "<api-key>"
    params = {
        'address': address,
        'key': google_api_key
    }
    url_params = urlencode(params)
    url = '{}?{}'.format(endpoint_url, url_params)
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    lat = result['results'][0]['geometry']['location']['lat']
    lng = result['results'][0]['geometry']['location']['lng']
    return (lat, lng)
```
