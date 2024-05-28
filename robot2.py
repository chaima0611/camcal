
def parse_args(x, y, theta):
        x_index = sys.argv.index('--x') if '--x' in sys.argv else None
        y_index = sys.argv.index('--y') if '--y' in sys.argv else None
        theta_index = sys.argv.index('--theta') if '--theta' in sys.argv else None
        
        x_command = float(sys.argv[x_index + 1]) if x_index is not None and x_index < len(sys.argv) else x
        y_command = float(sys.argv[y_index + 1]) if y_index is not None and y_index < len(sys.argv) else y
        theta_command = float(sys.argv[theta_index + 1]) if theta_index is not None and theta_index < len(sys.argv) else theta
        return x_command, y_command, theta_command


if __name__ == "__main__":
    bot = Rosmaster()
    bot.create_receive_threading()
    try:
        x, y, theta = initial_position()
        print("initial position: ", x, y, theta)
        target_x, target_y, target_theta = parse_args(x, y, theta)
        # target_theta = target_theta * 1000 * 3.14 / 180

        x_list, y_list, theta_list, vel_m1_list, vel_m2_list, vel_m3_list, vel_m4_list  = ctrl_robot_position(bot, target_x, target_y, target_theta, x, y, theta)

    except Exception:
        # Clear the cache data automatically sent by the MCU
        bot.clear_auto_report_data()

        # Restoring factory Settings
        bot.reset_flash_value()

        del bot

import serial

def receive_data_from_usart(port, baudrate, timeout):
    ser = serial.Serial(port, baudrate, timeout=timeout)
    
    try:
        while True:
            # Read bytes from serial port
            received_bytes = ser.read(6)  # Assuming you're sending 3 uint16_t values (6 bytes in total)
            
            # Check if any bytes are received
            if received_bytes:
                # Process received data (assuming it's in little-endian format)
                # Convert bytes to integers
                value1 = received_bytes[1] << 8 | received_bytes[0]
                value2 = received_bytes[3] << 8 | received_bytes[2]
                value3 = received_bytes[5] << 8 | received_bytes[4]
                
                # Print received values
                print("Received Values:")
                print(f"Value 1: {value1}")
                print(f"Value 2: {value2}")
                print(f"Value 3: {value3}")
    
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected. Exiting...")
    
    finally:
        # Close serial port
        ser.close()




try:
    while True:
        if ser.in_waiting > 0:
            # Read data from serial port
            data = ser.read_until()  # Read until a newline or timeout
            # Decode the received bytes into a string
            decoded_data = data.decode('utf-8').strip()
            print(f"Received data: {decoded_data}")

        # Optional: Add a small delay to prevent high CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting program")

finally:
    # Close the serial port
    ser.close()



# Unpack the four buffers of 20 bytes each
                unpacked_data1 = struct.unpack('5I', data[0:20])   # First 20 bytes
                unpacked_data2 = struct.unpack('5I', data[20:40])  # Next 20 bytes
                unpacked_data3 = struct.unpack('5I', data[40:60])  # Next 20 bytes
                unpacked_data4 = struct.unpack('5I', data[60:80])  # Last 20 bytes
                
                # Store the received data in a global variable
                received_data.append((unpacked_data1, unpacked_data2, unpacked_data3, unpacked_data4))

                # Optional: Add a small delay to prevent high CPU usage
                time.sleep(0.1)


while True:
        # Read 4 buffers of 4 bytes each
        data = ser.read(4 * 4)  # 4 buffers of 4 bytes each
        
        # Reconstruct signed integers
        integers = [int.from_bytes(data[i:i+4], byteorder='little', signed=True) for i in range(0, len(data), 4)]
        
        # Print received integers
        print("Received integers:", integers)
