import requests

def get_es_info():
    response = requests.post("https://api.kucoin.com/api/v1/bullet-public")
    if response.status_code == 200:
        json_response = response.json()
        token = json_response['data']['token']
        endpoint = json_response['data']['instanceServers'][0]['endpoint']
        return token, endpoint