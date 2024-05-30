data: b'\xaa\x01\x00d'
this is the function I use:
def read_int32_from_serial(data):
    # Read 4 bytes from the serial port
    # data = ser.read(4)
    print(len(data))
    if len(data) != 4:
        print("Error: Received incorrect number of bytes.")
        return None

    # Convert the bytes to a 32-bit signed integer (little-endian)
    value = struct.unpack('<i', data)[0]
    # print(f"Received value: {value}")
    return value

    
