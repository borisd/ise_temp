import time
import requests
from list_of_urls import decoders, encoders, device_url, request_url, encoder_ids, settings_body, netstat_body, temperature_body, findkey
from xyte import send_telemetry, get_command, update_command

def test_decoder(decoder):
    rc = send_telemetry(decoder, { "status": "online" })

    if rc['command']:
        handle_command(decoder)

def switch_command(decoder_id, encoder_id):
    payload = {
        "op": "join",
        "source_device": encoder_id,
        "stream_type": "HDMI",
        "stream_index": 0,
        "subscription_index": 0
    }

    rc = requests.post(url=device_url + str(decoder_id), json=payload)

    print("** Input switch command on " + decoder_id + " to " + encoder_id, rc)


def name_to_encoder_id(name):
    try:
        encoder = next(filter(lambda x: x['name'] == name, encoders))

    except:
        print('ERROR: Unknown encoder: ', name)
        return None

    return encoder['sdvoe_id']

def handle_command(decoder):
    command = get_command(decoder)

    print("** Got command: ", command)

    if command['name'] == 'cloud':
        target = command['parameters']['input']
        target_id = name_to_encoder_id(target)

        if target_id is None:
            return

        try:
            switch_command(decoder['sdvoe_id'], target_id)

        except:
            print("Something wrong switching commands")
            return

    update_command(decoder, 'done')

# Function for making API calls to the SDVoE API and parse the required information
def decoder_telemetries():
    for decoder in decoders:
        telemetry = prepare_telemetry(decoder['sdvoe_id'])

        if telemetry is None:
            print('Invalid telemetry for ', decoder['sdvoe_id'])
            continue

        rc = send_telemetry(decoder, telemetry)

        if rc['command']:
            handle_command(decoder)
        
def prepare_telemetry(decoder):
    try:

        telemetry_body = {}
        identity_get_request = requests.get(url=device_url+decoder)
        device_identity = identity_get_request.json()

        settings_post_request = requests.post(url=device_url+decoder, json=settings_body)
        device_settings = settings_post_request.json()
        nodes = settings_post_request.json()["result"]["devices"][0]["nodes"]

        netstat_post_request = requests.post(url=device_url+decoder, json=netstat_body)
        request_id = (netstat_post_request.json())["request_id"]
        netstat_get_request = requests.get(url=request_url+str(request_id))

        temperature_post_request = requests.post(url=device_url+decoder, json=temperature_body)
        temperature_request_id = (temperature_post_request.json())["request_id"]
        temperature_get_request = requests.get(url=request_url+str(temperature_request_id))

        telemetry_body["mac_address"] = device_identity["result"]["devices"][0]['nodes'][0]["status"]["mac_address"]
        telemetry_body["ip_address"] = device_identity["result"]["devices"][0]['nodes'][0]["status"]["ip"]["address"]
        telemetry_body["device_identity"] = device_settings["result"]["devices"][0]["identity"]["chipset_type"]
        telemetry_body["vendor_id"] = device_settings["result"]["devices"][0]["identity"]["vendor_id"]
        telemetry_body["product_id"] = device_settings["result"]["devices"][0]["identity"]["product_id"]
        telemetry_body["firmware_version"] = device_settings["result"]["devices"][0]["identity"]["firmware_version"]
        telemetry_body["is_active"] = device_settings["result"]["devices"][0]["status"]["active"]
        try:
            telemetry_body["bandwidth_usage"] = (netstat_get_request.json())["result"]["statistics"][0]["data_paths"][1]["bandwidth"]["usage"]["total"]
            telemetry_body["display_mode"] = list(findkey(nodes, 'display_mode'))[0]
            telemetry_body["device_temperature"] = (temperature_get_request.json())["result"]["devices"][0]["status"]["temperature"]

            print(telemetry_body)

        except:
            telemetry_body["bandwidth_usage"] = "Netstat details not available"
            telemetry_body["display_mode"] = "Display mode details not available"
            telemetry_body["device_temperature"] = "Temperature details unavailable"

        return telemetry_body

    except:

        telemetry_body = {
            "message": "Updating telemetries. Please wait"
        }

        return telemetry_body

def decoder_scheduler():
    try:
        print('Decoder scheduler started, ctrl-c to exit!')
        while 1:
            print("Sending decoder telemetries")
            decoder_telemetries()
            time.sleep(10)
            pass
        
    except KeyboardInterrupt:
        print('Decoder finished')

if __name__ == '__main__':
    test_decoder(decoders[0])