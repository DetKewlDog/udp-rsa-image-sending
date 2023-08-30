import socket, rsa
from PIL import Image
import DataHandler
from Constants import *


# SETTING UP SOCKET
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(RECEIVER_ADDRESS)

# SENDING PUBLIC RSA KEY
(public_key, private_key) = rsa.newkeys(RSA_KEYS_SIZE)
s.sendto((str(public_key.n) + KEYS_SEPERATOR + str(public_key.e)).encode(), SENDER_ADDRESS)

# RECEIVING THE IMAGE
chunks_count = int(s.recvfrom(4)[0].decode())

chunks = []
for i in range(chunks_count):
    chunks.append(s.recvfrom(BUFFER_SIZE)[0])

print('received', len(chunks), '/', chunks_count, 'chunks')

byte_stream = b''
for chunk in chunks:
    data = rsa.decrypt(chunk, private_key)
    byte_stream += data

img = DataHandler.deserialize_image(byte_stream)
img.show()