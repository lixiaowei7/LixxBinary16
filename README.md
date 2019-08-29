# LixxBinary16
A partial implementation of IEEE754 half-precision binary floating-point format: binary16.  
Endianness: **Little Endian**

### Lixx_Binary16
    >>> Lixx_Binary(65504).bytes
    b'\xff\x7b'
    >>> Lixx_Binary(b'\xff\x7b').value
    65504
