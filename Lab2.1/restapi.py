import os
import pprint
from os.path import dirname, join

import requests
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)

HOST = os.environ.get("HOST")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

headers = {
    "accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}


REST_OPER = "/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces"


if __name__ == "__main__":
    r = requests.get(
        "https://" + HOST + REST_OPER,
        verify=False,
        auth=(USERNAME, PASSWORD),
        headers=headers,
    )

    if r.status_code == 200:
        device_data = r.json()
        pprint.pprint(device_data, width=30)

        for current_int in device_data[
            "Cisco-IOS-XE-interfaces-oper:interfaces"
        ]["interface"]:
            print("Interface: ", current_int["name"])
            print(
                "Input packets/bytes: ",
                current_int["statistics"]["in-unicast-pkts"],
                "/",
                current_int["statistics"]["in-octets"],
            )
            print(
                "Output packets/bytes: ",
                current_int["statistics"]["out-unicast-pkts"],
                "/",
                current_int["statistics"]["out-octets"],
            )
