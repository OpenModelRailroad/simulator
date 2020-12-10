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

from bitstring import BitArray
from .mfx_exception import MFXAddressToBigException


class MFXPacketFactory(object):
    """
    MFX Package builder
    """

    @staticmethod
    def function_package_short(address, f1, f2, f3, f4):
        address_binary = BitArray('uint:8=%d' % address)

    def create_address(self, address):
        """
        10      AAAAAAA         7 Bit Adresse   max 127
        110     AAAAAAAAA       9 Bit Adresse   max 511
        1110    AAAAAAAAAAA     11 Bit Adresse  max 2047
        1111    AAAAAAAAAAAAAA  14 Bit Adresse  max 16383
        """
        if 0 < address < 128:
            pass
        elif 127 < address < 512:
            pass
        elif 511 < address < 2048:
            pass
        elif 2047 < address < 16384:
            pass
        else:
            raise MFXAddressToBigException
