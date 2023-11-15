import socket
# import colorsys # for HSV-to-RGB-conversion
BRIGHTNESS = 1.0
GAMMA = 1.0


def prepare_message(data, gamma=GAMMA):
    """Prepares the pixel data for transmission over UDP
    """
    # 4 bytes for future use as a crc32 checksum in network byte order.
    checksum = bytearray([0,0,0,0])
    data_as_bytes = bytearray()
    for row in data:
        for pixel in row:
            r = int(((pixel.r/255.0) ** gamma) * 255 * BRIGHTNESS)
            g = int(((pixel.g/255.0) ** gamma) * 255 * BRIGHTNESS)
            b = int(((pixel.b/255.0) ** gamma) * 255 * BRIGHTNESS)
            data_as_bytes += bytearray([r,g,b])
            
    while len(data_as_bytes) < 1920:
        data_as_bytes += bytearray([0,0,0])
    
    message = data_as_bytes + checksum
    return message


def blank_screen(rows=16, cols=40):
    checksum = bytearray([0,0,0,0])
    data_as_bytes = bytearray()
    for _ in range(rows * cols):
        data_as_bytes += bytearray([0, 0, 0])
    message = data_as_bytes + checksum
    return message

def send_array(data, hostname, udp_port=1337):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (hostname, udp_port))
