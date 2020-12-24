def xor_bytes(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


if __name__ == "__main__":
    print("testing xor")
    byte1 = b'00000101'
    byte2 = b'01100100'
    checksum = b'01100001'

    print(xor_bytes(byte1, byte2))

    rte = int.from_bytes(xor_bytes(byte1, byte2), byteorder='big')
    rtc = int.from_bytes(checksum, byteorder='big')


    print(format(ord(xor_bytes(byte1, byte2)), 'X'))

    print(rte == rtc)
