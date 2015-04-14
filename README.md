#otpBthDriver
A commandline tool to retrieve and parse Bluetooth LE device information for the Trustware system. It will print out the info of any devices in physical proximity.

Dependencies:
- Python: sudo apt-get install python
- Linux Bluetooth stack: sudo apt-get install libbluetooth-dev

To use:
- Start sending advertisement packets from a Bluetooth LE device with data "TOTP UID URL"
 - Without quotes and without spaces
 - TOTP: time-based OTP using 30-second intervals (6 characters)
 - UID: unique ID assigned to this device at manufacture time (8 chars)
 - URL: web address of the company authentication server (12 chars)
- sudo python main.py
