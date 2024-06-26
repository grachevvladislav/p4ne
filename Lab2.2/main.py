import glob
import re
from ipaddress import IPv4Interface
from os.path import basename

from flask import Flask, jsonify

files = glob.glob("./data/*.log")

app = Flask(__name__)


def return_network(s):
    r = re.search(
        "ip address ((?:[0-9]{1,3}[.]?){4}) ((?:[0-9]{1,3}[.]?){4})", s
    )
    if r is not None:
        return IPv4Interface((r.group(1), r.group(2)))
    else:
        return None


@app.route("/")
def index():
    info = "Hello, world!"
    return info


@app.route("/configs")
def configs():
    hosts = [basename(i) for i in files]
    return jsonify(hosts)


@app.route("/configs/<host>")
def config(host):
    networks = []
    for file in files:
        if host in file:
            with open(file, "r") as f:
                for line in f:
                    network = return_network(line)
                    if network is not None:
                        networks.append(str(return_network(line)))
    return jsonify(networks)


if __name__ == "__main__":
    app.run(debug=True)
