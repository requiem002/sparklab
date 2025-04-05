import serial
import time

# Adjust COM port and baud rate as needed
SERIAL_PORT = "COM5"  # e.g., "/dev/ttyUSB0" on Linux/mac
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Wait for Arduino to reboot

current_user = None

def read_serial():
    if ser.in_waiting > 0:
        line = ser.readline().decode("utf-8").strip()
        return line
    return None

def send_drawer_command(drawer_name):
    command = f"DRAWER:{drawer_name}\n"
    ser.write(command.encode())

def main():
    global current_user
    print("Server started. Waiting for RFID login...\n")

    while True:
        msg = read_serial()
        # print(msg)
        if msg:
            if msg.startswith("RFID:"):
                current_user = msg.split(":")[1]
                print(f"\n🪪  User logged in: {current_user}")
                print("RFID scan processed")  # Debugging message
                request_component()

            if msg.startswith("CLOSED:"):
                    drawer = msg.split(":")[1]
                    print(f"✅ Drawer {drawer} closed.")
                    print("Drawer Closed. Ready for new action or RFID scan...\n")
                    print(f"Drawer {drawer} has been closed successfully.")  # Debugging message

            elif msg.startswith("ALERT:"):
                drawer = msg.split(":")[1]
                print(f"⚠️ ALERT: Drawer {drawer} open for too long!")

def request_component():
    global current_user
    drawer = input("Enter drawer to access (A0, A1, B0, etc.) or 'logout': ").strip().upper()
    print(drawer,end="")     

    if drawer == "LOGOUT":
            print("🔓 User logged out.\n")
            current_user = None
            print("Waiting for new RFID scan...\n")
    send_drawer_command(drawer)
    print(f"🔦 Sent drawer command for: {drawer}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        ser.close()
