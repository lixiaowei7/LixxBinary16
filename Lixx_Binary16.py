# <Lixx_Binary16, a paritial implemention of IEEE binary16.>
# Copyright (C) <2018>  <Xiaowei Li>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# @Email: Xiaowei Li<lixiaowei7@live.cn>
# @Reference: https://en.wikipedia.org/wiki/Half-precision_floating-point_format#ARM_alternative_half-precision

import struct

SIGN_BITS = 1
EXPONENT_BITS = 5
FRACTION_BITS = 10

class Lixx_Binary16:
    """partial implemention"""

    def __init__(self, number):
        self.value = None
        self.bytes = None

        if type(number) in (int, float):
            self.value = number
            self.cover()
        elif type(number) == bytes:
            self.bytes = number
            self.reveal()
        else:
            raise ValueError("invalid number type:", type(number))

    def __str__(self):
        return self.bytes.hex()

    # ToDo: subnormal number
    def reveal(self):
        """bytes to number"""
        x = struct.unpack("<H", self.bytes)[0]

        sign = x >> 15
        exponent = (x & int('0111110000000000', 2)) >> 10
        significant = x & int('0000001111111111', 2)

        self.value = (-1) ** sign * 2 ** (exponent - 15) * (1 + significant / 1024)

    def _inte(self, inte):
        assert inte <= 65504

        s = ''
        if inte == 0:
            s += '0'
            return s
        elif inte == 1:
            s += '1'
            return s
        
        s += self._inte(inte >> 1)
        if inte % 2 == 0:
            s += '0'
        elif inte % 2 == 1:
            s += '1'
        
        return s

    # ToDo: subnormal number
    def _frac(self, value):
        frac = value - int(value)

        if frac < 0.000061035:
            return '0'

        n = 0
        s = ''
        while (frac >= 0.000061035):
            n += 1
            if frac >= 1 / 2 ** n:
                s += '1'
                frac -= 1 / 2 ** n
            else:
                s += '0'

        return s

    def cover(self):
        """number to bytes"""

        value = self.value
        sign = 0 if value >= 0 else 1

        value = abs(value)
        inte = self._inte(int(value))
        frac = self._frac(value)

        s = inte + "." + frac
        index_one = s.find("1")
        index_dot = s.find(".")

        if index_one != -1:
            exponent = index_dot - index_one
            if '1' in inte:
                exponent -= 1
            exponent += (2 ** 4 - 1)
        else:
            exponent = 0

        if index_dot > index_one:
            s = s.replace(".", "")
        fraction = "{0:0<10}".format(s[index_one + 1:index_one + 11])

        self.bytes = struct.pack("<H", (sign << 15) + (exponent << 10) + int(fraction, 2))