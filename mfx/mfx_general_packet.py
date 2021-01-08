from bitstring import BitArray
import sys

from mfx import MFXException


class MFXGeneralPacket(object):
    praeamble = BitArray('0b01110')

    def __init__(self, address_byte, data_bytes):

        self.address_byte = BitArray(address_byte)
        self.data_bytes = map(BitArray, data_bytes)
        if sys.version_info.major >= 3:
            self.data_bytes = list(self.data_bytes)

    @staticmethod
    def from_bit_array(int_array):
        packet = BitArray(int_array)
        ct = 0
        n = 0
        start = 0
        for b in packet:
            if b == 1:
                ct += 1
            if ct == 3:
                if b == 0:
                    start = n + 1
            n += 1

        print('START OF ADDRESS %d' % start)

        addr_length = 0

        print([1, 0, 0, 0])

        address_byte = 0  # TODO get the Address

        aps = packet[start:start + 4].bin
        print(aps)
        print(aps == '0b1000')

        if aps == 1000:
            address_start = start + 2
            address_end = address_start + 7
            address_byte = packet[address_start:address_end]

            print(address_start)
            print(address_end)
            print(address_byte)

        elif aps == 1100:
            address_start = start + 3
            address_end = address_start + 9
            address_byte = packet[address_start:address_end]

            print(address_start)
            print(address_end)
            print(address_byte)

        elif aps == 1110:
            address_start = start + 4
            address_end = address_start + 11
            address_byte = packet[address_start:address_end]

            print(address_start)
            print(address_end)
            print(address_byte)
        elif aps == 1111:
            address_start = start + 4
            address_end = address_start + 14
            address_byte = packet[address_start:address_end]

            print(address_start)
            print(address_end)
            print(address_byte)
        else:
            raise MFXException

        data_bytes = []  # todo get the data bytes

        dbit = 0
        data_bytes_a = []
        while dbit < len(data_bytes):
            data_bytes_a.append(data_bytes[dbit:dbit + 8])
            dbit += 9  # start bit to next byte
        # return MFXGeneralPacket(address_byte, data_bytes_a)

    '''
    def to_bit_array(self):
        packet = BitArray()

        packet.append(self.praeamble)
        packet.append(self.address_byte)

        for byte in self.data_bytes:
            packet.append(byte)
        return map(int, packet)
    '''
    '''
    def to_bit_string(self):
        return "".join(map(str, self.to_bit_array()))
    '''

    def __str__(self):
        return "Device #%d: %s" % (self.address_byte.uint, " ".join(map(str, self.data_bytes)))
