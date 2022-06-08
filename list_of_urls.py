# This file contains constants such as URL's and device ID's. Also contains a function which is used in
# both encoder and decoder programs.

# Base url for making get and post requests to the SDVoE API server. Change the IP address in the below string
# accordingly.
base_url = "http://192.168.1.99:8080/api/"
device_url = base_url + "device/"
request_url = base_url + "request/"
xyte_url = "https://hub.xyte.io/v1/devices/"

# Device ID's of encoders
encoders = [
    { "sdvoe_id": "5410EC31A05F", "xyte_id": "03147fc1-19c6-4936-b16d-3e98e27eef5c", "xyte_auth": "6891845ea53a7bd05ce9490cc0bfd905", "name": "Amsterdam" },
    { "sdvoe_id": "5410EC318C27", "xyte_id": "17908287-176c-427e-b0c7-2284551f57ae", "xyte_auth": "de7e93b5ece30a2d71e2bf40e15c0f84", "name": "Kitten" },
    { "sdvoe_id": "801F1243BB51", "xyte_id": "04de4d28-7df2-40f3-b93f-75287478b470", "xyte_auth": "69408af3e49d0d2a61e26b702d4014b8", "name": "Pattern" },
    { "sdvoe_id": "801F12433B92", "xyte_id": "4f4d7275-0886-4354-b81b-a2624900380a", "xyte_auth": "ada71f0ea91e423674a2fcd95bd1edfc", "name": "Ski" }
]

# Device ID's of decoders.
decoders = [
    { "sdvoe_id": "801F12431454", "xyte_id": "19b10b88-50c8-411f-8f40-da37a46d006a", "xyte_auth": "3ed1bdeae6be7082d5ca53c2d9f21584" },
    { "sdvoe_id": "801F12433D36", "xyte_id": "5a444f39-ff84-4046-a101-c38b01ff703e", "xyte_auth": "632eae7a6154f15dfe95cc3b1489e9f7" },
    { "sdvoe_id": "801F1243B9B7", "xyte_id": "9855aece-a4a7-4bf6-a80c-5ee470e7b2bd", "xyte_auth": "ef129177ccf134caccca514e1e2651bb" },
    { "sdvoe_id": "801F12430AC6", "xyte_id": "4fffac6f-b9b0-46bd-9aed-672e4da201c0", "xyte_auth": "0b728c4b6b9182c04180c6bf6864c45b" }
]

encoder_ids = {
    "Amsterdam": "801F12433D36",
    "Kitten": "5410EC31A05F",
    "Pattern": "801F12430AC6",
    "Ski": "801F1243B9B7"
}

# Bodies of POST requests for retrieving settings, netstat details and temperature details respectively.

settings_body = {
    "op":"get",
    "subset":"settings"
}

netstat_body = {
    "op": "netstat",
    "option": "read"
}

temperature_body = {
    "op":"get",
    "subset":"temperature"
}

# Function for finding a particular key from a dictionary


def findkey(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in findkey(i, kv):
               yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in findkey(j, kv):
                yield x

