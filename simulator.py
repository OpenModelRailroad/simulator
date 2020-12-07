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

    def __init__(self, random_sleep, ht):
        self.factory = DCCPacketFactory()
        self.random_sleep = random_sleep
        if ht:
            self.hostname = ht
        else:
            self.hostname = 'simulator'

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect(('localhost', 11337))
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
            packet_object = {
                "type": "dcc",
                "raw": bit_string
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
    args = parser.parse_args()

    print(args)

    simulator = Simulator(args.random, args.name)
    print(simulator)
    simulator.start()
