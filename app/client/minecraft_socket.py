from app.client import varint

def decodeMCPacket(packet):
    length, data = varint.separate_first_varint_and_the_rest(packet)
    # len(None) throws an error
    if data is not None and len(data) == length:
        return data
    else:
        return None

class MinecraftSocket:

    def __init__(self, socket):
        self.socket = socket

    def send(self, data):
        size_header = varint.encode(len(data))
        packet = size_header + data
        while len(packet) > 0:
            bytes_sent = self.socket.send(packet)
            packet = packet[bytes_sent:]
        #print('Sent %r' % (size_header + data))

    def recv(self):
        size = self.recv_varint()
        data = self.recv_bytes(size)
        return data

    def recv_varint(self):
        received_bytes = []
        while not varint.check_encoded(received_bytes):
            received_bytes += self.socket.recv(1)
        return varint.decode_no_check(received_bytes)

    def recv_bytes(self, size):
        frames = []
        while size > 0:
            received = self.socket.recv(min(size, 4096))
            size -= len(received)
            frames.append(received)
        return b''.join(frames)
