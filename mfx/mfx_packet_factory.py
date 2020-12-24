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

from bitstring import BitArray, Bits
from .mfx_exception import MFXAddressToBigException


class MFXPacketFactory(object):
    """
    MFX Package builder
    """
    sync_pattern = BitArray('0b01110')

    def drive_short(self, reverse=0, step=0):
        command_prefix = 0b000
        pass

    def drive(self, reverse=0, step=0):
        command_prefix = 0b001
        pass

    def function_short(self, address, f0=0, f1=0, f2=0, f3=0):
        command_prefix = 0b010
        address_binary = self.create_address(address)
        function_binary = BitArray(0b0000)
        command_bit = BitArray(self.sync_pattern)

        if f3 is 1:
            function_binary = function_binary | 0b1000
        if f2 is 1:
            function_binary = function_binary | 0b0100
        if f1 is 1:
            function_binary = function_binary | 0b0010
        if f0 is 1:
            function_binary = function_binary | 0b0001

        command_bit.append(address_binary)
        command_bit.append(function_binary)

        print(command_bit.bin)
        # command_bit.append(address_binary)

    def function_expanded(self, f0=0, f2=0, f3=0, f1=0, f4=0, f5=0, f6=0, f7=0, f8=0, f9=0, f10=0, f11=0, f12=0, f13=0,
                          f14=0, f15=0):
        command_prefix = 0b011
        pass

    def set_function(self, fnum=0, f=0):
        command_prefix = 0b100

    def decoder_search(self):
        command = '11101000000000000000000000000000000000000000'
        return command

    def create_address(self, address):
        """
        10      AAAAAAA         7 Bit Adresse   max 127
        110     AAAAAAAAA       9 Bit Adresse   max 511
        1110    AAAAAAAAAAA     11 Bit Adresse  max 2047
        1111    AAAAAAAAAAAAAA  14 Bit Adresse  max 16383
        """
        bitaddr = BitArray()

        if 0 < address < 128:
            # bitaddr.join('0b10')
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

        return bitaddr
