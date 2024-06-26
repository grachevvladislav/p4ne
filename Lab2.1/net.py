import os
import re
import time
from os.path import dirname, join

import paramiko
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)
HOST = os.environ.get("HOST")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


def net_command(session, cmd, timeout=1):
    buf_size = 65536
    session.send("\n")
    session.recv(buf_size)
    if cmd[:-1] != "\n":
        cmd = cmd + "\n"
    session.send(cmd)
    time.sleep(timeout)
    return session.recv(buf_size).decode()


def disable_scrolling(session):
    return net_command(session, "terminal length 0")


if __name__ == "__main__":
    with paramiko.SSHClient() as ssh_connection:
        ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_connection.connect(
            HOST,
            username=USERNAME,
            password=PASSWORD,
            look_for_keys=False,
            allow_agent=False,
        )
        session = ssh_connection.invoke_shell()
        disable_scrolling(session)
        lines = net_command(session, "show interfaces", timeout=3).split("\n")

        for line in lines:
            data = re.match("^([A-Z].+?) is", line)
            if data:
                print("Interface " + data.group(1))
                continue
            data = re.match("^.+?([0-9]+) packets input, ([0-9]+) bytes", line)
            if data:
                print(
                    "Packets/bytes input: ", data.group(1), "/", data.group(2)
                )
                continue
            data = re.match(
                "^.+?([0-9]+) packets output, ([0-9]+) bytes", line
            )
            if data:
                print(
                    "Packets/bytes output: ", data.group(1), "/", data.group(2)
                )
