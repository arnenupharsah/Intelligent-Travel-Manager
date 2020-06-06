import requests
import json


def recommend(startPOI,length):
    params = {'startPOI': startPOI,'length':length} 
    requests.post('http://0.0.0.0:8080', data=json.dumps(params))
    #return p.json()
    #return params

