from mfx import MFXPacketFactory

if __name__ == "__main__":
    factory = MFXPacketFactory()
    factory.function_short(15000, 0, 1, 0, 1)
