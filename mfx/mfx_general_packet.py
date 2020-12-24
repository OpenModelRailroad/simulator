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

import sys
from bitstring import BitArray


class MFXGeneralPackage(object):

    def __init__(self, address_bytes, data_bytes=[]):
        self.praeamble = BitArray('0b01110')
        self.address_bytes = BitArray(address_bytes)
        self.data_bytes = map(BitArray, data_bytes)
        if sys.version_info.major >= 3:
            self.data_bytes = list(self.data_bytes)

    @staticmethod
    def from_bit_array(int_array):
        packet = BitArray(int_array)

    def to_bit_array(self):
        packet = BitArray()
        packet.append(self.praeamble)
        packet.append(self.address_bytes)
        for byte in self.data_bytes:
            packet.append(byte)
        return map(int, packet)

    def to_bit_string(self):
        return "".join(map(str, self.to_bit_array()))

    def __str__(self):
        return "Device #%d: %s" % (self.address_bytes.uint, " ".join(map(str, self.data_bytes
                                                                          )))
