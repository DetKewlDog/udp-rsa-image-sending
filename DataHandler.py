from PIL import Image
from io import BytesIO

def serialize_image(img, chunk_size):
    byte_stream = BytesIO()
    img.save(byte_stream, format=img.format)
    byte_stream = byte_stream.getvalue()
    for i in range(0, len(byte_stream), chunk_size):
        yield byte_stream[i:i + chunk_size]

def deserialize_image(byte_stream):
    return Image.open(BytesIO(byte_stream))