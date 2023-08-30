import socket, rsa
from PIL import Image
import DataHandler
from Constants import *


# SERIALIZING IMAGE
img = Image.open('img.png')
chunks = list(DataHandler.serialize_image(img, IMAGE_CHUNK_SIZE))

# SETTING UP SOCKET
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(SENDER_ADDRESS)

# RECEIVING REMOTE PUBLIC RSA KEY
n, e = [int(i) for i in s.recvfrom(RSA_KEYS_SIZE)[0].decode().split(KEYS_SEPERATOR)]
remote_key = rsa.PublicKey(n, e)

# SENDING THE IMAGE
chunks_count = len(chunks)
s.sendto(str(chunks_count).encode(), RECEIVER_ADDRESS)

for chunk in chunks:
    encrypted_chunk = rsa.encrypt(chunk, remote_key)
    s.sendto(encrypted_chunk, RECEIVER_ADDRESS)

print('sent', len(chunks), 'chunks')