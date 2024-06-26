import glob
from os.path import dirname, join

if __name__ == "__main__":
    ip = set()
    for current_file_name in glob.glob(
        join(dirname(__file__), "../data/*.log")
    ):
        with open(current_file_name) as f:
            for current_line in f:
                if current_line.find("ip address") == 1:
                    ip.add(current_line.replace("ip address", "").strip())

    for i in ip:
        print(i)
