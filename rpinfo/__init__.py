#!/usr/bin/env python3
"""
rpinfo 0.2.1 (2019.06.03)

Gathers platform information of the currently running Raspberry Pi.
Supports: Raspberry Pi A, A+, B, B+, 2B, 3B, 3B+, Zero, ZeroW, CM1 and CM3.

(C) 2018,2019 @TimothyBrown

MIT License
"""
import os

class RaspberryPi:
    """
    A class to provide revision, model, chipset, manufacturer, memory and serial number of the
    currently running Raspberry Pi. Returns None if not running on a Pi.
    """
    def __init__(self):
        # Return None if we're not running on a Pi.
        self.revision = None
        self.model = None
        self.processor = None
        self.manufacturer = None
        self.memory = None
        self.serial = None

        # Location of the `cpuinfo` data.
        cpuinfo_file = '/proc/cpuinfo'
        code = None
        # Table to decode new style revision code values.
        new_style = {
        'model': {0x0: 'A', 0x1: 'B', 0x2: 'A+', 0x3: 'B+', 0x4: '2B', 0x5: 'Prototype', 0x6: 'CM1', 0x8: '3B', 0x9: 'Zero', 0xA: 'CM3', 0xC: 'Zero W', 0xD: '3B+'},
        'processor': {0: 'BCM2835', 1: 'BCM2836', 2: 'BCM2837'},
        'manufacturer': {0: 'Sony UK', 1: 'Egoman', 2: 'Embest', 3: 'Sony Japan', 4: 'Embest', 5: 'Stadium'},
        'memory': {0: '256 MB', 1: '512 MB', 2: '1 GB'}
        }
        # Table to decode old style revision codes.
        old_style = {
        0x02: ('1.0','B', 'BCM2835', 'Egoman', '256 MB'),
        0x03: ('1.0', 'B', 'BCM2835', 'Egoman', '256 MB'),
        0x04: ('2.0', 'B', 'BCM2835', 'Sony UK', '256 MB'),
        0x05: ('2.0', 'B', 'BCM2835', 'Qisda', '256 MB'),
        0x06: ('2.0', 'B', 'BCM2835', 'Egoman', '256 MB'),
        0x07: ('2.0', 'A', 'BCM2835', 'Egoman', '256 MB'),
        0x08: ('2.0', 'A', 'BCM2835', 'Sony UK', '256 MB'),
        0x09: ('2.0', 'A', 'BCM2835', 'Qisda', '256 MB'),
        0x0d: ('2.0', 'B', 'BCM2835', 'Egoman', '512 MB'),
        0x0e: ('2.0', 'B', 'BCM2835', 'Sony UK', '512 MB'),
        0x0f: ('2.0', 'B', 'BCM2835', 'Egoman', '512 MB'),
        0x10: ('1.0', 'B+', 'BCM2835', 'Sony UK', '512 MB'),
        0x11: ('1.0', 'CM1', 'BCM2835', 'Sony UK', '512 MB'),
        0x12: ('1.1', 'A+', 'BCM2835', 'Sony UK', '256 MB'),
        0x13: ('1.2', 'B+', 'BCM2835', 'Embest', '512 MB'),
        0x14: ('1.0', 'CM1', 'BCM2835', 'Embest', '512 MB'),
        0x15: ('1.1', 'A+', 'BCM2835', 'Embest', '512 MB'),
        }

        try:
        # Try to open the `cpuinfo` file and iterate through it...
            with open(cpuinfo_file) as f:
                for line in f:
                    # ...and look for the `Revision` tag starting a line.
                    if line.startswith('Revision'):
                        # If we find it, split it at the colon, strip EOL characters and
                        # convert it to an int.
                        code = int(line.split(':', 1)[1].strip()[-6:], 16)
                    # While we're looping through the lines, we might as well grab the serial too.
                    if line.startswith('Serial'):
                        self.serial = line.split(':', 1)[1].strip()[-8:].upper()
        except FileNotFoundError:
        # I guess the file doesn't exsist. Oh well!
            pass

        # If we found something, let's process it.
        if code is not None:
            # The first bit of the second byte tells us if this is a new style or old style revision code.
            if bool(code >> 23 & 0x000000001):
                try:
                    # The revision number consists of the last 4 bits of the last byte.
                    self.revision = '1.{}'.format(code & 0b00000000000000000000000000001111)
                    # The model consists of the next 8 bits.
                    self.model = new_style['model'][code >> 4 & 0b0000000000000000000011111111]
                    # The processor make up the next 4 bits.
                    self.processor = new_style['processor'][code >> 12 & 0b00000000000000001111]
                    # The manufacturer make up the next 4 bits.
                    self.manufacturer = new_style['manufacturer'][code >> 16 & 0b0000000000001111]
                    # The memory capacity make up the next three bits.
                    self.memory = new_style['memory'][code >> 20 & 0b000000000111]
                except KeyError:
                    self.revision = None
                    self.model = None
                    self.processor = None
                    self.manufacturer = None
                    self.memory = None
                    self.serial = None
            # If not, we've got an old style revision code.
            else:
                try:
                    self.revision, self.model, self.processor, self.manufacturer, self.memory = old_style[code]
                except KeyError:
                    self.revision = None
                    self.model = None
                    self.processor = None
                    self.manufacturer = None
                    self.memory = None
                    self.serial = None

if __name__ == '__main__':
    print("*** Raspberry Pi Info ***")
    rpi = RaspberryPi()
    print("Revision:", rpi.revision)
    print("Model:", rpi.model)
    print("Processor:", rpi.processor)
    print("Manufacturer:", rpi.manufacturer)
    print("Memory:", rpi.memory)
    print("Serial:", rpi.serial)
