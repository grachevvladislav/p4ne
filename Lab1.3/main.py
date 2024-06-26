from pysnmp.hlapi import *

if __name__ == "__main__":
    snmp_name = ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)
    snmp_interfaces = ObjectIdentity("1.3.6.1.2.1.2.2.1.2")
    target = UdpTransportTarget(("10.31.70.209", 161))

    names = getCmd(
        SnmpEngine(),
        CommunityData("public", mpModel=0),
        target,
        ContextData(),
        ObjectType(snmp_name),
    )

    interfaces = nextCmd(
        SnmpEngine(),
        CommunityData("public", mpModel=0),
        target,
        ContextData(),
        ObjectType(snmp_interfaces),
        lexicographicMode=False,
    )

    for answer in names:
        for value in answer[3]:
            print(value)

    for answer in interfaces:
        for value in answer[-1]:
            print(value)
