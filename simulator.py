"""
    Copyright (C) 2020  OpenModelRailRoad, Florian Thiévent

    This file is part of "OMRR".

    "OMRR" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "OMRR" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import time

from dccpi import *
from time import sleep
from random import randint, uniform
import argparse
import uuid
import re
import socket
import json
import sys


class Simulator:
    ip = socket.gethostbyname(socket.gethostname())
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    hostname = ''
    factory = None
    random_sleep = False
    sock = None
    protocol = ''
    mfxfunc = [
        '011101000001011001000000010110101110',
        '011101000000101001001000000000110101110',
        '01110100000101000001000000110101110',
        '01110100000101000010000000110101110',
        '00001110110111110100010101110000'
    ]

    def __init__(self, logserver_ip, random_sleep, ht, protocol):
        self.logserver_ip = logserver_ip
        self.factory = DCCPacketFactory()
        self.random_sleep = random_sleep
        self.protocol = protocol
        if ht:
            self.hostname = ht
        else:
            self.hostname = 'simulator'

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((self.logserver_ip, 11337))
        self.start()

    def __str__(self):
        str = """Simulator
    ip: %s
    mac: %s
    hostname: %s
    random sending: %s
        """
        return str % (self.ip, self.mac, self.hostname, self.random_sleep)

    def send(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            else:
                print("sent %s to %s [%d bytes]" % (msg, self.sock.getsockname(), sys.getsizeof(msg)))
            totalsent = totalsent + sent

    def send_heartbeat(self):
        msg = {'type': 'heartbeat', 'ip': self.ip, 'mac': self.mac, 'hostname': self.hostname}
        self.send(json.dumps(msg).encode('utf-8'))

    def start(self):
        self.send_heartbeat()
        start_time = int(round(time.time() * 1000))

        while True:

            if (int(round(time.time() * 1000)) - start_time) > 10000:
                self.send_heartbeat()
                start_time = int(round(time.time() * 1000))

            msg_type = uniform(0.0, 3.5)
            packet = None
            type_string = ""

            if msg_type < 2.0:
                type_string = "SPEED"
                address = randint(1, 20)
                speed = randint(0, 14)
                speed_steps = randint(1, 14)
                direction = randint(0, 1)
                packet = self.factory.speed_and_direction_packet(address=address, speed=speed, speed_steps=speed_steps,
                                                                 direction=direction)
            elif 2.0 <= msg_type < 2.5:
                type_string = "IDLE"
                packet = self.factory.idle_packet()
            elif 2.5 <= msg_type < 3.0:
                type_string = "STOP"
                packet = self.factory.stop_packet()
            elif 3.0 <= msg_type < 3.5:
                type_string = "RESET"
                packet = self.factory.reset_packet()

            bit_string = packet.to_bit_string()

            # TODO change back dude
            if self.protocol == 'dcc':
                packet_object = {
                    "type": "dcc",
                    "raw": bit_string
                }
            else:
                packet_object = {
                    "type": "mfx",
                    "raw": self.mfxfunc[randint(0, 4)]
                }

            # print("sending %s packet:\t%s " % (type_string, bit_string))
            self.send(json.dumps(packet_object).encode('utf-8'))

            if self.random_sleep:
                st = uniform(0.1, 1.0)
                sleep(st)
            else:
                sleep(0.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--random', help='randomise time between packages. intervall is between 0.1 and 1.0 sec',
                        action='store_true', required=False)
    parser.add_argument('-n', '--name', help='name of simulator', required=False)
    parser.add_argument('-p', '--protocol', help='dcc or mfx. default is randomized between these two protocol',
                        required=False, default='dcc')
    parser.add_argument('-l', '--logserver', help='ip address of logserver', required=False, default='localhost')
    args = parser.parse_args()

    print(args)
    simulator = Simulator(args.logserver, args.random, args.name, args.protocol)
    print(simulator)
    simulator.start()
