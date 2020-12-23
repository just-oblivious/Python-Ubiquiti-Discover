# Python Ubiquiti Discover

Simple Python implementation of the Ubiquiti device discovery protocol.

The protocol was "reverse engineered" by capturing traffic from the "WiFiman" Android app, payload decoding is best-effort and not guaranteed to be correct.

**Usage:** `python3 ubnt-discover.py {device-ip-address}`

*Default is to broadcast on 255.255.255.255*
