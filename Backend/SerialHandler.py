import serial
import time

class ArduinoCommunicator:
    def __init__(self, serial_port, baud_rate=9600, timeout=1):
        """
        Initializes the ArduinoCommunicator with the serial port and baud rate.

        Args:
            serial_port (str): The serial port the Arduino is connected to (e.g., 'COM3' on Windows, '/dev/ttyACM0' on Linux).
            baud_rate (int): The baud rate for serial communication (default: 9600).
            timeout (int): Timeout in seconds for serial operations (default: 1).
        """
        try:
            self.serial_port = serial.Serial(serial_port, baud_rate, timeout=timeout)
            time.sleep(2)  # Give Arduino time to initialize
            print(f"Connected to Arduino on {serial_port}")
        except serial.SerialException as e:
            print(f"Error connecting to Arduino on {serial_port}: {e}")
            self.serial_port = None

    def __def__(self):
        """
        Destructor to close the serial connection when the object is deleted.
        """
        self.close()
        
    def send_command(self, command):
        """
        Sends a command to the Arduino.

        Args:
            command (str): The command string to send.
        """
        if self.serial_port and self.serial_port.is_open:
            command_with_newline = command + '\n'
            try:
                self.serial_port.write(command_with_newline.encode('utf-8'))
                print(f"Sent command: {command}")
            except serial.SerialException as e:
                print(f"Error sending command '{command}': {e}")
        else:
            print("Serial port is not open.")

    def read_output(self, timeout=1):
        """
        Reads output from the Arduino until a newline character is received or timeout.

        Args:
            timeout (int): Timeout in seconds for reading (default: 1).

        Returns:
            str: The received output from the Arduino, or None if no output within the timeout.
        """
        if self.serial_port and self.serial_port.is_open:
            start_time = time.time()
            output = b''
            while True:
                if self.serial_port.in_waiting > 0:
                    char = self.serial_port.read(1)
                    output += char
                    if char == b'\n':
                        return output.decode('utf-8').strip()
                if time.time() - start_time > timeout:
                    if output:
                        return output.decode('utf-8').strip()
                    return None
        else:
            print("Serial port is not open.")
            return None

    def turn_on_led(self, drawer_location):
        """
        Sends a command to the Arduino to turn on the LED for a specific drawer.

        Args:
            drawer_location (int): The location ID of the drawer.
        """
        command = f"LED{drawer_location}"
        self.send_command(command)

    def get_arduino_response(self, timeout=2):
        """
        Reads and prints all available output from the Arduino for a given timeout.

        Args:
            timeout (int): Maximum time to wait for responses (default: 2 seconds).
        """
        if self.serial_port and self.serial_port.is_open:
            start_time = time.time()
            while time.time() - start_time < timeout:
                if self.serial_port.in_waiting > 0:
                    line = self.serial_port.readline().decode('utf-8').strip()
                    if line:
                        print(f"Arduino says: {line}")
                time.sleep(0.1) # Small delay to avoid busy-waiting
        else:
            print("Serial port is not open.")

    def close(self):
        """
        Closes the serial connection.
        """
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            print("Serial port closed.")
        else:
            print("Serial port was not open.")

if __name__ == '__main__':
    # Replace 'YOUR_SERIAL_PORT' with the actual serial port of your Arduino
    arduino_port = 'YOUR_SERIAL_PORT'
    communicator = ArduinoCommunicator(arduino_port)

    if communicator.serial_port:
        try:
            # Example usage:
            drawer_to_turn_on = 1
            communicator.turn_on_led(drawer_to_turn_on)
            communicator.get_arduino_response(timeout=3) # Wait for Arduino's response

            drawer_to_turn_on = 3
            communicator.turn_on_led(drawer_to_turn_on)
            communicator.get_arduino_response(timeout=3)

            # You can add more interactions here

        except KeyboardInterrupt:
            print("\nExiting.")
        finally:
            communicator.close()