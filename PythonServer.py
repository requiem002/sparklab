import serial
import time

# Adjust COM port and baud rate as needed
SERIAL_PORT = "COM5"  # e.g., "/dev/ttyUSB0" on Linux/mac
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Wait for Arduino to reboot

current_user = None
authorized_rfid = "7770F3A0"  # Only allow this RFID

def read_serial():
    if ser.in_waiting > 0:
        line = ser.readline().decode("utf-8").strip()
        return line
    return None

def send_drawer_command(drawer_name):
    command = f"DRAWER:{drawer_name}\n"
    ser.write(command.encode())

def is_valid_drawer(drawer_name):
    valid_drawers = ["A0", "A1", "B0", "B1"]
    return drawer_name in valid_drawers

def main():
    global current_user
    print("Server started. Waiting for RFID login...\n")

    while True:
        msg = read_serial()
        if msg:
            # Process RFID scans only if no one is currently logged in.
            if msg.startswith("RFID:"):
                if current_user is None:
                    current_user = msg.split(":")[1]
                    print(f"\n🪪  User logged in: {current_user}")
                    print("RFID scan processed")  # Debugging message

                    # Only allow access if the RFID matches the authorized one.
                    if current_user == authorized_rfid:
                        print("RFID is authorized.")
                        request_component()
                    else:
                        print("❌ Access Denied. Unauthorized RFID.")
                        current_user = None  # Reset user if not authorized

            elif msg.startswith("CLOSED:"):
                drawer = msg.split(":")[1]
                print(f"✅ Drawer {drawer} closed.")
                print(f"Drawer {drawer} has been closed successfully.")  # Debugging message
                print("Ready for new action or RFID scan...\n")

            elif msg.startswith("ALERT:"):
                drawer = msg.split(":")[1]
                print(f"⚠️ ALERT: Drawer {drawer} open for too long!")

def request_component():
    global current_user
    drawer = input("Enter drawer to access (A0, A1, B0, B1) or 'logout': ").strip().upper()
    if drawer == "LOGOUT":
        print("🔓 User logged out.\n")
        current_user = None
        print("Waiting for new RFID scan...\n")
    else:
        while not is_valid_drawer(drawer):
            print("❌ Drawer does not exist. Please enter a valid drawer name.")
            drawer = input("Enter drawer to access (A0, A1, B0, B1) or 'logout': ").strip().upper()
        send_drawer_command(drawer)
        print(f"🔦 Sent drawer command for: {drawer}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        ser.close()
