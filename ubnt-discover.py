"""
Author: D. van Gent
License: MIT

Description: Simple Python implementation of the Ubiquiti device discovery protocol.
The protocol was "reverse engineered" by capturing traffic from the "WiFiman" Android app,
payload decoding is best-effort and not guaranteed to be correct.

Usage: python3 ubnt-discover.py {ip-address}
(default is to broadcast on 255.255.255.255)
"""

import socket
import sys
from ipaddress import IPv4Address


def ubnt_discover(addr):
    ''' Send discovery packets to Ubnt device '''
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(3)

        for i in range(0, 3):  # send sequential packets to UBNT device
            port = 10001 if i else 5678  # switch ports, this mimics "WiFiman" app behavior
            sock.sendto(i.to_bytes(4, byteorder='little'), (addr, port))

        reply, srcaddr = sock.recvfrom(1024)
        dvc_data = []
        offset = 4  # data fields start at position 4 in the reply

        while offset < len(reply):
            ftype, dlength = reply[offset], reply[offset + 2]  # field type, payload length
            offset += 3
            dvc_data.append((ftype, reply[offset:offset + dlength]))
            offset += dlength

        return dvc_data, srcaddr[0]


if __name__ == '__main__':
    addr = sys.argv[1] if len(sys.argv) == 2 else '255.255.255.255'
    dvc_data, dvc_addr = ubnt_discover(addr)
    print(f' Reply from: {dvc_addr}')

    # decode the fields
    fields = {
        None: ('Unknown', lambda d: ' '.join(f'{b:02x}' for b in d)),
        0x01: ('HW addr', lambda d: ':'.join(f'{b:02x}' for b in d)),
        0x02: ('Address', lambda d: f"{':'.join(f'{b:02x}' for b in d[0:6])} \
({IPv4Address(d[6:10])})"),
        0x03: ('Firmware', lambda d: d.decode()),
        0x0a: ('Uptime', lambda d: f"{int.from_bytes(d, byteorder='big')} seconds"),
        0x0b: ('Hostname', lambda d: d.decode()),
        0x0c: ('Model', lambda d: d.decode())

    }
    for field, data in dvc_data:
        name, decode = fields.get(field, fields[None])
        print(f'{name:>11s}: {decode(data)}')

    # Just for fun: grab the first global/WAN IP
    # This could be useful for dynamic DNS updates (through the API of your domain provider)
    for f, d in dvc_data:
        if f == 0x02:
            ip = IPv4Address(d[6:10])
            if ip.is_global:
                print(f'     WAN IP: {ip}')
                break
