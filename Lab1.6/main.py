import glob
import re
from ipaddress import IPv4Interface
from os.path import dirname, join


def classify(s):
    data = re.match(
        r"^ ip address ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+) ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)",
        s,
    )
    if data:
        return {
            "ip": IPv4Interface(str(data.group(1)) + "/" + str(data.group(2)))
        }

    data = re.match(r"^interface (.+)", s)
    if data:
        return {"int": data.group(1)}

    data = re.match(r"^hostname (.+)", s)
    if data:
        return {"host": data.group(1)}

    return ("UNCLASSIFIED",)


if __name__ == "__main__":
    ip_addresses, interfaces, hosts = [], [], []

    for current_file_name in glob.glob(
        join(dirname(__file__), "../data/*.log")
    ):
        with open(current_file_name) as f:
            for current_line in f:
                c = classify(current_line)
                if "ip" in c:
                    ip_addresses.append(c)
                elif "int" in c:
                    interfaces.append(c)
                elif "host" in c:
                    hosts.append(c)

    print(ip_addresses)
    print(interfaces)
    print(hosts)
