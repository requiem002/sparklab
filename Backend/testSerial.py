from SerialHandler import *

def test_serial_handler():
    
    Serial = ArduinoCommunicator(serial_port='COM15', baud_rate=9600)
    # Serial.connect()
    Serial.turn_on_led("1")

if __name__ == "__main__":
    test_serial_handler()