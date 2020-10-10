
class Piece:
    def __init__(self, inBuffer, offset, length):
        self.inBuffer = inBuffer
        self.offset = offset
        self.length = length
        

    def __repr__(self):
        return str(self.inBuffer) + "-" + str(self.offset) + "-" + str(self.length)
