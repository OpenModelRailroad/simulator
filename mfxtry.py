from mfx import MFXGeneralPacket
from mfx.mfx_packet import MFXPacket

if __name__ == "__main__":
    praeambel = 0b01110

    broadcast_address = 0b000000000000000000

    chks = 0b00000000

    mfxpacket = MFXPacket(6)

    richtung = 1
    command = 0b010
    command_string = mfxpacket.get_command_name(command)
    fahrstufe = 7  # 0-8
    function = 'F7'
    function_value = 1
    bin_fahrstufe = mfxpacket.calc_drivingstep(fahrstufe)

    address_str = str(mfxpacket.create_address(500)).replace('0b', '')

    print(fahrstufe)
    print(bin_fahrstufe)
    print(command_string)

    print('addr: %s' % mfxpacket.create_address(500))
    print(len(address_str))

    print(mfxpacket.get_direction_string(0))
    print('{}:{:08b}_{}_{:03b}_{:01b}_{}'.format(mfxpacket.get_command_name_constant(command), praeambel, address_str, command, richtung,
                                                 mfxpacket.calc_drivingstep(fahrstufe)))

    pkg = MFXGeneralPacket.from_bit_array([0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0])
    print(pkg)
