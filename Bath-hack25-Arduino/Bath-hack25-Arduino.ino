#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);

#define NUM_DRAWERS 4

const int ledPins[NUM_DRAWERS] = {2, 3, 4, 5};
const int hallPins[NUM_DRAWERS] = {A0, A1, A2, A3};

String drawerNames[NUM_DRAWERS] = {"A0", "A1", "B0", "B1"};
String authorizedRFID = "7770F3A0";  // Only this RFID is authorized

unsigned long openTime[NUM_DRAWERS] = {0};
unsigned long lastBlink[NUM_DRAWERS] = {0};
bool isDrawerOpen[NUM_DRAWERS] = {false};
bool alertSent[NUM_DRAWERS] = {false};
bool ledState[NUM_DRAWERS] = {false};

const unsigned long TIMEOUT = 30000;  // 30 seconds timeout (adjust as needed)
const unsigned long BLINK_INTERVAL = 500;  // LED blink speed in ms

String lastRFID = "";

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();

  for (int i = 0; i < NUM_DRAWERS; i++) {
    pinMode(ledPins[i], OUTPUT);
    pinMode(hallPins[i], INPUT_PULLUP); // Assuming active LOW
    digitalWrite(ledPins[i], LOW);
  }

  Serial.println("Smart Organizer Ready. Waiting for RFID...");
}

void loop() {
  checkRFID();
  handleDrawerCommands();
  monitorDrawers();
}

// Returns the index of the drawer name or -1 if not found.
int getDrawerIndex(String name) {
  for (int i = 0; i < NUM_DRAWERS; i++) {
    if (drawerNames[i] == name) {
      return i;
    }
  }
  return -1;
}

void checkRFID() {
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String rfid = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      rfid += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
      rfid += String(mfrc522.uid.uidByte[i], HEX);
    }
    rfid.toUpperCase();

    if (rfid == authorizedRFID) {  // Only allow access for this RFID
      Serial.print("RFID:");
      Serial.println(rfid);
      lastRFID = rfid;
      Serial.println("Authorized RFID detected. Proceed with drawer selection.");
    } else {
      Serial.print("RFID:");
      Serial.println(rfid);
      Serial.println("Unauthorized RFID detected. Access denied.");
      lastRFID = "";  // Reset lastRFID if unauthorized
    }
    delay(1000);
  }
}

void handleDrawerCommands() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.startsWith("DRAWER:")) {
      String drawerName = input.substring(7);
      int index = getDrawerIndex(drawerName);
      if (index != -1) {
        digitalWrite(ledPins[index], HIGH);
        ledState[index] = true;
        openTime[index] = millis();
        lastBlink[index] = millis();
        isDrawerOpen[index] = true;
        alertSent[index] = false;
      } else {
        Serial.print("Invalid drawer: ");
        Serial.println(drawerName);
      }
    }
  }
}

void monitorDrawers() {
  for (int i = 0; i < NUM_DRAWERS; i++) {
    bool drawerClosed = digitalRead(hallPins[i]) == LOW;

    if (isDrawerOpen[i]) {
      if (drawerClosed) {
        isDrawerOpen[i] = false;
        digitalWrite(ledPins[i], LOW);
        Serial.print("CLOSED:");
        Serial.println(drawerNames[i]);
        Serial.println("Drawer Closed");
        alertSent[i] = false;
        ledState[i] = false;
        delay(1000);  // Small delay to ensure it's fully closed before restarting
        Serial.println("Waiting for new RFID scan...");
        lastRFID = "";  // Reset the last RFID to force the next scan
      } else {
        if (!alertSent[i] && millis() - openTime[i] > TIMEOUT) {
          Serial.print("ALERT:");
          Serial.println(drawerNames[i]);
          alertSent[i] = true;
        }

        if (alertSent[i]) {
          if (millis() - lastBlink[i] >= BLINK_INTERVAL) {
            ledState[i] = !ledState[i];
            digitalWrite(ledPins[i], ledState[i]);
            lastBlink[i] = millis();
          }
        }
      }
    }
  }
}

void requestComponent() {
  Serial.println("Enter drawer to access (A0, A1, B0, etc.) or 'logout': ");
}
