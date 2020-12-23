# Python Ubiquiti Discover

Simple Python implementation of the Ubiquiti device discovery protocol.

The protocol was "reverse engineered" by capturing traffic from the "WiFiman" Android app, payload decoding is best-effort and not guaranteed to be correct.

**Usage:** `python3 ubnt-discover.py {device-ip-address}`

*Default is to broadcast on 255.255.255.255*

## Sample output
```plain
$ python3 ubnt-discover.py
 Reply from: 172.16.10.1
    Address: fc:ec:da:be:ef:b3 (172.16.10.1)
    Address: fc:ec:da:be:ef:b5 (123.45.56.89)
    Address: fc:ec:da:be:ef:b3 (10.0.0.1)
    HW addr: fc:ec:da:be:ef:b0
     Uptime: 432694 seconds
   Hostname: edgerouter
      Model: ER-6P
   Firmware: EdgeRouter.ER-e300.v2.0.8.5247496.191120.1124
    Unknown: 00 00 00 00
     WAN IP: 123.45.56.89
```

```plain
$ python3 ubnt-discover.py 192.168.2.254
 Reply from: 192.168.2.254
    Address: f0:9f:c2:fa:ce:a0 (192.168.2.254)
    HW addr: f0:9f:c2:fa:ce:9f
     Uptime: 165 seconds
   Hostname: ubnt
      Model: ERLite-3
   Firmware: EdgeRouter.ER-e100.v2.0.8.5247496.191120.1124
```
