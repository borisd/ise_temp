import requests
from list_of_urls import xyte_url

def send_telemetry(device, telemetry):
    print("\n")
    print("> Sending telemetry to: " + device['xyte_id'], telemetry)

    data = { "status": "online", "telemetries": telemetry }
    url = xyte_url + device['xyte_id'] + "/telemetry"
    headers = { "Authorization": device['xyte_auth'] }

    rc = requests.post(url=url, json=data, headers=headers).json()

    print("< Got: ", rc)

    return rc

def get_command(device):
    url = xyte_url + device['xyte_id'] + "/command"
    headers = { "Authorization": device['xyte_auth'] }

    return requests.get(url=url, headers=headers).json()

def update_command(device, status):
    url = xyte_url + device['xyte_id'] + "/command"
    headers = { "Authorization": device['xyte_auth'] }
    data = { "status": status }

    return requests.post(url=url, json=data, headers=headers).json()