/*
  Face Scanner - ESP32 OLED Display
  ==================================
  Receives serial commands from face_scanner.py and displays
  access status on a 0.96" SSD1306 OLED (128x64, I2C).

  Wiring:
    OLED SDA -> GPIO 21
    OLED SCL -> GPIO 22
    OLED VCC -> 3.3V
    OLED GND -> GND

  Required Libraries (install via Arduino Library Manager):
    - Adafruit SSD1306
    - Adafruit GFX Library

  Serial Protocol:
    "READY"              -> System ready / monitoring
    "GRANTED:<username>" -> Access granted
    "DENIED:<reason>"    -> Access denied
    "OFFLINE"            -> System shutting down
*/

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

String inputBuffer = "";
unsigned long lastMessageTime = 0;
unsigned long displayDuration = 4000; // ms to show granted/denied
bool showingResult = false;

void setup() {
  Serial.begin(115200);

  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println("SSD1306 allocation failed");
    for (;;); // Halt
  }

  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  showStartup();
}

void loop() {
  // Read serial data
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      processCommand(inputBuffer);
      inputBuffer = "";
    } else if (c != '\r') {
      inputBuffer += c;
    }
  }

  // Return to idle after displaying result
  if (showingResult && (millis() - lastMessageTime > displayDuration)) {
    showingResult = false;
    showMonitoring();
  }
}

void processCommand(String cmd) {
  cmd.trim();
  if (cmd.length() == 0) return;

  if (cmd == "READY") {
    showMonitoring();
  }
  else if (cmd.startsWith("GRANTED:")) {
    String username = cmd.substring(8);
    showAccessGranted(username);
    showingResult = true;
    lastMessageTime = millis();
  }
  else if (cmd.startsWith("DENIED:")) {
    String reason = cmd.substring(7);
    showAccessDenied(reason);
    showingResult = true;
    lastMessageTime = millis();
  }
  else if (cmd == "OFFLINE") {
    showOffline();
  }
}

void showStartup() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(20, 10);
  display.println("FACE SCANNER");
  display.setCursor(30, 30);
  display.println("Starting...");
  display.setCursor(15, 50);
  display.println("Waiting for PC");
  display.display();
}

void showMonitoring() {
  display.clearDisplay();

  // Header
  display.setTextSize(1);
  display.setCursor(20, 0);
  display.println("FACE SCANNER");

  // Divider line
  display.drawLine(0, 12, 128, 12, SSD1306_WHITE);

  // Eye icon (simple ASCII art via text)
  display.setTextSize(1);
  display.setCursor(40, 20);
  display.println("(O) (O)");

  // Status
  display.setTextSize(1);
  display.setCursor(18, 38);
  display.println("Monitoring...");

  display.setCursor(15, 52);
  display.println("Show your face");

  display.display();
}

void showAccessGranted(String username) {
  display.clearDisplay();

  // Draw border
  display.drawRect(0, 0, 128, 64, SSD1306_WHITE);
  display.drawRect(2, 2, 124, 60, SSD1306_WHITE);

  // Checkmark area
  display.setTextSize(2);
  display.setCursor(52, 5);
  display.println("[/]");

  // ACCESS GRANTED
  display.setTextSize(1);
  display.setCursor(12, 28);
  display.println("ACCESS GRANTED!");

  // Divider
  display.drawLine(10, 40, 118, 40, SSD1306_WHITE);

  // Username
  display.setTextSize(2);
  // Center the username
  int16_t x = (128 - (username.length() * 12)) / 2;
  if (x < 0) x = 0;
  display.setCursor(x, 46);
  display.println(username);

  display.display();
}

void showAccessDenied(String reason) {
  display.clearDisplay();

  // Draw border
  display.drawRect(0, 0, 128, 64, SSD1306_WHITE);

  // X mark
  display.setTextSize(2);
  display.setCursor(52, 5);
  display.println("[X]");

  // ACCESS DENIED
  display.setTextSize(1);
  display.setCursor(16, 28);
  display.println("ACCESS DENIED!");

  // Divider
  display.drawLine(10, 40, 118, 40, SSD1306_WHITE);

  // Reason
  display.setTextSize(1);
  int16_t x = (128 - (reason.length() * 6)) / 2;
  if (x < 0) x = 0;
  display.setCursor(x, 48);
  display.println(reason);

  display.display();
}

void showOffline() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(25, 20);
  display.println("SYSTEM OFFLINE");
  display.setCursor(20, 40);
  display.println("Disconnected");
  display.display();
}
