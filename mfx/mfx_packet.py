from bitstring import BitArray

from mfx import MFXAddressToBigException, MFXException, MFXBitsForFunctionNotFound

MFX_COMMANDS = [
    (0b000, 'DRIVE_SHORT', 'drive (short)', 'Fahren (kurz)'),
    (0b001, 'DRIVE', 'drive', 'Fahren'),
    (0b010, 'FUNCTION_SHORT', 'function (short)', 'Funktionen (kurz)'),
    (0b011, 'FUNCTION_EXTENDED', 'function (extended)', 'Funktionen (erweitert)'),
    (0b100, 'FUNCTION_INDIVIDUAL', 'function (individual)', 'Funktionen (Einzelansteuerug)'),
    (0b101, 'RESERVED', 'reserved', 'Reserviert'),
    (0b110, 'RESERVED', 'reserved', 'Reserviert'),
    (0b111, 'CONFIGURATION', 'configuration', 'Konfiguration')
]

MFX_CONFIG_COMMANDS = [
    (0b000, 'read cv', 'CV lesen'),
    (0b001, 'write cv', 'CV schreiben'),
    (0b010, 'decoder search', 'Decoder Suche'),
    (0b011, 'assign track address', 'Zuweisung Schienenadresse'),
    (0b100, 'mfx ping', 'mfx Ping'),
    (0b101, 'Central', 'Zentrale'),
    (0b110, 'reserved', 'reserviert'),
    (0b111, 'reserved', 'reserviert')
]


class MFXPacket:
    address = 0
    address_bin = 0b0
    praeambel = 0b01110

    def __init__(self, address=0):
        self.set_address(address)

    # Getter and Setter
    def get_address(self):
        return self.address

    def get_address_bin(self):
        return self.address_bin

    def set_address(self, address):
        self.address = address
        self.address_bin = self.create_address(address)

    # String Methods
    def get_packet_string(self):
        return "not yet implemented"

    # Class Methods
    def get_command_bits(self, func_name):
        for c in MFX_COMMANDS:
            if func_name in c:
                return c[0]

        return None

    def get_command_name(self, bits):
        for c in MFX_COMMANDS:
            if bits in c:
                return c[2]
        return None

    def get_command_name_constant(self, bits):
        for c in MFX_COMMANDS:
            if bits in c:
                return c[1]
        return None

    def calc_drivingstep(self, stufe):
        return self.decimal_to_binary(stufe * 16)

    def decimal_to_binary(self, n):
        return '{:08b}'.format(n)

    def is_emergency_stop(self, step) -> bool:
        if step is 1:
            return True
        return False

    def get_direction_string(self, direction):
        if direction is 0:
            return "forward"
        return "backward"

    def create_address(self, address):
        """
        10  AAAAAAA         7 Bit Adresse   max 127
        110  AAAAAAAAA       9 Bit Adresse   max 511
        1110  AAAAAAAAAAA     11 Bit Adresse  max 2047
        1111  AAAAAAAAAAAAAA  14 Bit Adresse  max 16383
        """
        bitaddr = BitArray()

        if 0 < address < 128:
            bitaddr.append('uint:2=%d' % 2)
            bitaddr.append('uint:7=%d' % address)
        elif 127 < address < 512:
            bitaddr.append('uint:3=%d' % 6)
            bitaddr.append('uint:9=%d' % address)
            pass
        elif 511 < address < 2048:
            bitaddr.append('uint:4=%d' % 14)
            bitaddr.append('uint:11=%d' % address)
            pass
        elif 2047 < address < 16384:
            bitaddr.append('uint:4=%d' % 15)
            bitaddr.append('uint:14=%d' % address)
            pass
        else:
            raise MFXAddressToBigException

        return bitaddr.bin
