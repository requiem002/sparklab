#include <MFRC522.h>
#include <MFRC522Extended.h>
#include <require_cpp11.h>

#include <MFRC522.h>
#include <SPI.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);

#define NUM_DRAWERS           4
#define DRAWER_ARRAY_WIDTH    2
#define DRAWER_ARRAY_HEIGHT   2

const int ledPins[NUM_DRAWERS] = {2, 3, 4, 5};
const int hallPins[NUM_DRAWERS] = {A0, A1, A2, A3};
struct cmdMemory {
  uint8_t prevDrawerLocation = false;
  bool checkDrawer = false;
  bool turnOffLEDFlag = false;
};


const uint8_t drawerLocations[NUM_DRAWERS] = {
  // 0b00000000, // Drawer 1
  // 0b00000001, // Drawer 2
  // 0b00010000, // Drawer 3
  // 0b00010001, // Drawer 4
  0b00000001, // Drawer 1
  0b00000010, // Drawer 2
  0b00000011, // Drawer 3
  0b00000100, // Drawer 4
};

cmdMemory cmdMem;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  mfrc522.PCD_Init();
  SPI.begin();
  for (int i = 0; i < NUM_DRAWERS; i++) {
    pinMode(ledPins[i], OUTPUT);
    pinMode(hallPins[i], INPUT_PULLUP);
    digitalWrite(ledPins[i], LOW); // Initialize LEDs to off
  }
  
}

void loop() {
  // put your main code here, to run repeatedly:
  checkRFID();
  Serial.println("AAAAA");
  cmdMem =  commandHandler();
  Serial.println("BBBB");
  drawerHandler();
  }


bool turnOnLED(uint8_t drawerLocation) {
  // Turn on the LED for the specified drawer
  for (int i = 0; i < NUM_DRAWERS; i++) {
    if (drawerLocations[i] == drawerLocation) {
      digitalWrite(ledPins[i], HIGH);
      return true;
    }
  }
  return false;
}

bool turnOffLED(uint8_t drawerLocation) {
  // Turn off the LED for the specified drawer
  for (int i = 0; i < NUM_DRAWERS; i++) {
    if (drawerLocations[i] == drawerLocation) {
      digitalWrite(ledPins[i], LOW);
      return true;
    }
  }
  return false;
}

bool isDrawerOpen(uint8_t drawerLocation) {
  // Check if the drawer is present using the hall effect sensor
  for (int i = 0; i < NUM_DRAWERS; i++) {
    if (drawerLocations[i] == drawerLocation) {
      return digitalRead(hallPins[i]); 
    }
  }
  return false;
}

void checkRFID() {
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String rfid = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      rfid += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
      rfid += String(mfrc522.uid.uidByte[i], HEX);
    }
    rfid.toUpperCase();

    Serial.print("RFID:");
    Serial.println(rfid);
    // Check if the RFID is authorized
    delay(100);
  }
}

cmdMemory commandHandler(){
  if(Serial.available()){
    String command = Serial.readStringUntil('\n');
    if(command.startsWith("LED")){
      uint8_t drawerLocation = command.substring(3).toInt();
      if(!isDrawerOpen(drawerLocation)){
        turnOnLED(drawerLocation);
        cmdMem.prevDrawerLocation = drawerLocation; 
        cmdMem.checkDrawer = true;
        
        Serial.print("LED,");
        Serial.print(drawerLocation);
        Serial.println(" turned on");
      } else { 
        cmdMem.prevDrawerLocation = drawerLocation; 
        cmdMem.turnOffLEDFlag = true;
        
        Serial.print("LED, ");
        Serial.print(drawerLocation);
        Serial.println(" not turned on. Drawer Already opened");
      }
    }
    else {
      Serial.println("Invalid command");
    }
  }
  return cmdMem;
}

void drawerHandler(){
  // Check if the drawer LED needs to be reset after drawer selection
  if (cmdMem.checkDrawer) {
    // Check if the drawer is open using the hall effect sensor
    if (isDrawerOpen(cmdMem.prevDrawerLocation)) {
      cmdMem.turnOffLEDFlag = true;
      Serial.print("Drawer, ");
      Serial.print(cmdMem.prevDrawerLocation);
      Serial.println(" not turned on. Drawer Already opened ");
    } else if(!isDrawerOpen(cmdMem.prevDrawerLocation) && cmdMem.turnOffLEDFlag) {
      turnOffLED(cmdMem.prevDrawerLocation);
      cmdMem.turnOffLEDFlag = false;
      cmdMem.checkDrawer = false;
 
      Serial.print("Drawer, ");
      Serial.print(cmdMem.prevDrawerLocation);
      Serial.println(" closed");
      
      
    }
  } 
}