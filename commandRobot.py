import serial
import time

# Open serial port (change port name and baud rate as needed)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

def send_command(command_type, value):
    header = 0xAA
    cmd_type = command_type & 0xFF
    value_H = (value >> 8) & 0xFF
    value_L = value & 0xFF
    checksum = (header + cmd_type + value_H + value_L) % 256

    packet = bytearray([header, cmd_type, value_H, value_L, checksum])

    ser.write(packet)

# Example usage
send_command(1, 100)  # Send command type 1 with value 100

# Read response from microcontroller
response = ser.readline().strip()
print("Response:", response)

# Close serial port
ser.close()
