import time
import requests
from list_of_urls import encoders, device_url, request_url, settings_body, temperature_body, findkey
from xyte import send_telemetry

# Function for making API calls to the SDVoE API and parse the required information.
def encoder_telemetries():
    print(" - Sending telemetries -")
    for encoder in encoders:
        telemetry = prepare_telemetry(encoder['sdvoe_id'])

        if telemetry is None:
            print("Could not get telemetry for: ", encoder['sdvoe_id'])
        else:
            send_telemetry(encoder, telemetry)

def prepare_telemetry(encoder):
    try:

        telemetry_body = {}
        identity_get_request = requests.get(url=device_url+encoder)
        device_identity = identity_get_request.json()

        settings_post_request = requests.post(url=device_url+encoder, json=settings_body)
        device_settings = settings_post_request.json()
        nodes = settings_post_request.json()["result"]["devices"][0]["nodes"]
        required_field = list(filter(lambda details: details['type'] == 'HDMI_DECODER', nodes))[0]

        temperature_post_request = requests.post(url=device_url + encoder, json=temperature_body)
        temperature_request_id = (temperature_post_request.json())["request_id"]
        temperature_get_request = requests.get(url=request_url + str(temperature_request_id))

        telemetry_body["mac_address"] = device_identity["result"]["devices"][0]['nodes'][0]["status"]["mac_address"]
        telemetry_body["ip_address"] = device_identity["result"]["devices"][0]['nodes'][0]["status"]["ip"]["address"]
        telemetry_body["device_identity"] = device_settings["result"]["devices"][0]["identity"]["chipset_type"]
        telemetry_body["vendor_id"] = device_settings["result"]["devices"][0]["identity"]["vendor_id"]
        telemetry_body["product_id"] = device_settings["result"]["devices"][0]["identity"]["product_id"]
        telemetry_body["firmware_version"] = device_settings["result"]["devices"][0]["identity"]["firmware_version"]
        telemetry_body["is_active"] = device_settings["result"]["devices"][0]["status"]["active"]
        try:
            telemetry_body["source_resolution"] = str(required_field["status"]["video"]["width"]) + "*" \
                                                    + str(required_field["status"]["video"]["width"])
            telemetry_body["source_video_frame_rate"] = required_field["status"]["video"]["frames_per_second"]
            telemetry_body["source_color_space"] = required_field["status"]["video"]["color_space"]
            telemetry_body["bits_per_pixel"] = required_field["status"]["video"]["bits_per_pixel"]
            telemetry_body["scan_mode"] = required_field["status"]["video"]["scan_mode"]

            telemetry_body["stream_0_status"] = device_settings["result"]["devices"][0]["streams"][0]["status"]["state"]
            telemetry_body["stream_0_address"] = device_settings["result"]["devices"][0]["streams"][0]["configuration"]["address"]
            telemetry_body["stream_0_enable"] = device_settings["result"]["devices"][0]["streams"][0]["configuration"]["enable"]
            telemetry_body["stream_0_index"] = device_settings["result"]["devices"][0]["streams"][0]["index"]
            telemetry_body["stream_0_type"] = device_settings["result"]["devices"][0]["streams"][0]["type"]

            telemetry_body["stream_1_status"] = device_settings["result"]["devices"][0]["streams"][1]["status"]["state"]
            telemetry_body["stream_1_address"] = device_settings["result"]["devices"][0]["streams"][1]["configuration"]["address"]
            telemetry_body["stream_1_enable"] = device_settings["result"]["devices"][0]["streams"][1]["configuration"]["enable"]
            telemetry_body["stream_1_index"] = device_settings["result"]["devices"][0]["streams"][1]["index"]
            telemetry_body["stream_1_type"] = device_settings["result"]["devices"][0]["streams"][1]["type"]

            telemetry_body["stream_0"] = "Details sent"
            telemetry_body["stream_1"] = "Details sent"

            telemetry_body["hdcp_version"] = list(findkey(nodes, 'hdcp_version'))[0]
            telemetry_body["device_temperature"] = (temperature_get_request.json())["result"]["devices"][0]["status"]["temperature"]

        except:
            telemetry_body["stream_0"] = "Details unavailable"
            telemetry_body["stream_1"] = "Details unavailable"
            telemetry_body["hdcp_version"] = "Details unavailable"
            telemetry_body["device_temperature"] = "Temperature details unavailable"

        return telemetry_body

    except:

        telemetry_body = {
            "message": "Updating telemetries. Please wait"
        }

        return telemetry_body

def encoder_scheduler():
    try:
        print('Encoder scheduler started, ctrl-c to exit!')
        while 1:
            encoder_telemetries()
            time.sleep(10)
    except:
        print("Finished encoder scheduler")



