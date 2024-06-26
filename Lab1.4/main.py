import random
from ipaddress import IPv4Network

NET = random.randint(0x0B000000, 0xDF000000)
MASK = random.randint(8, 24)


class IPv4RandomNetwork(IPv4Network):
    def __init__(self, p_start=0, p_end=32):
        IPv4Network.__init__(
            self,
            (
                random.randint(0x0B000000, 0xDF000000),
                random.randint(p_start, p_end),
            ),
            strict=False,
        )

    def regular(self):
        return self.is_global and not (
            self.is_multicast
            or self.is_link_local
            or self.is_loopback
            or self.is_private
            or self.is_reserved
            or self.is_unspecified
        )

    def key_value(self):
        return int(self.network_address) + (int(self.netmask) << 32)


def sortfunc(x):
    return x.key_value()


if __name__ == "__main__":
    random.seed()

    data = []

    while len(data) < 50:
        random_network = IPv4RandomNetwork(8, 24)
        if random_network.regular() and random_network not in data:
            data.append(random_network)

    for n in sorted(data, key=sortfunc):
        print(n)
