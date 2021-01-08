class MFXException(Exception):
    def __init__(self, message="An unknown mfx Error occured"):
        self.message = message
        super().__init__(self.message)


class MFXAddressToBigException(MFXException):
    def __init__(self, message="Address for mfx is to big, can only be 16383 max."):
        self.message = message
        super().__init__(self.message)


class MFXBitsForFunctionNotFound(MFXException):
    def __init__(self, message="Could not find any bits for function"):
        self.message = message
        super().__init__(self.message)
