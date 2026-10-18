# 🛒 ESP32 Door Control Hardware Shopping List

## Complete Hardware Requirements for Face Recognition Door Access System

---

## 📦 **ESSENTIAL COMPONENTS**

### 1. **ESP32 Development Board** ⭐ **REQUIRED**

**Recommended Model: ESP32-DevKitC-32E or ESP32-WROOM-32**

**Why this model:**
- Built-in WiFi (2.4 GHz)
- Built-in Bluetooth
- 30+ GPIO pins
- 3.3V logic (compatible with most relays)
- USB-C or Micro-USB for programming
- Low power consumption
- Cheap (~$5-10)

**Specifications:**
- **MCU:** ESP32-D0WDQ6 (dual-core, 240MHz)
- **WiFi:** 802.11 b/g/n
- **Bluetooth:** 4.2 BR/EDR and BLE
- **GPIO:** 34 programmable pins
- **Operating Voltage:** 3.3V
- **Input Voltage:** 5V (via USB) or 7-12V (via VIN pin)
- **Current:** ~80mA (active), ~10µA (deep sleep)

**Where to buy:**
- Amazon: Search "ESP32 DevKitC"
- AliExpress: Search "ESP32 WROOM-32"
- Local electronics stores

**Price:** $5-10 USD

---

### 2. **Relay Module** ⭐ **REQUIRED**

**Recommended: 1-Channel 5V Relay Module (Optocoupler)**

**Why this model:**
- Optocoupler isolation (protects ESP32 from high voltage)
- 5V logic compatible (works with ESP32's 3.3V via level shifter OR use 3.3V relay)
- Can switch up to 10A @ 250V AC or 10A @ 30V DC
- LED indicator for relay status
- Screw terminals for easy wiring

**Specifications:**
- **Operating Voltage:** 5V (or 3.3V version available)
- **Trigger Current:** ~20mA
- **Max Switching:** 10A @ 250V AC / 10A @ 30V DC
- **Isolation:** Optocoupler (2500V)
- **Connections:** VCC, GND, IN (signal), COM, NO, NC

**Alternative:** If you can't find 3.3V relay, use a **Logic Level Converter (Bi-Directional)** between ESP32 and 5V relay.

**Where to buy:**
- Amazon: "1 channel relay module 5V"
- AliExpress: "1 channel relay module optocoupler"

**Price:** $2-5 USD

---

### 3. **Power Supply for ESP32** ⭐ **REQUIRED**

**Option A: USB Power Adapter (Recommended for testing)**
- **Specs:** 5V, 1A minimum
- **Connector:** USB-A to Micro-USB or USB-C (match your ESP32)
- **Price:** $3-5 USD

**Option B: AC-DC Adapter (For permanent installation)**
- **Specs:** 5V, 2A (for reliability)
- **Connector:** Barrel jack or direct wire
- **Price:** $5-10 USD

**Option C: Power over GPIO (Advanced)**
- Use ESP32's VIN pin (accepts 7-12V)
- Requires voltage regulator (built into most ESP32 boards)

---

### 4. **Jumper Wires** ⭐ **REQUIRED**

**Recommended: Male-to-Female Jumper Wires (Dupont wires)**

**Why:**
- Easy connections without soldering
- Reusable
- Multiple lengths available

**What you need:**
- **10-20 pieces** of Male-to-Female wires
- **Colors:** Red (VCC), Black (GND), Yellow/Green (Signal)
- **Length:** 20cm or 30cm

**Where to buy:**
- Amazon: "Dupont jumper wires male to female"
- AliExpress: "jumper wires 40 pin"

**Price:** $2-5 USD

---

### 5. **Electric Strike Lock** ⭐ **REQUIRED**

**Recommended: 12V DC Electric Strike Lock (Fail-Safe or Fail-Secure)**

**Types:**
- **Fail-Safe:** Unlocks when power is cut (fire safety) - **Recommended for most doors**
- **Fail-Secure:** Locks when power is cut (maximum security)

**Specifications:**
- **Voltage:** 12V DC (most common) or 24V DC
- **Current:** 500mA - 1A (check your specific model)
- **Holding Force:** 1200-1500 lbs (standard)
- **Mounting:** Mortise or surface mount

**Popular Models:**
- **Securitron MPS-12V** (12V, 500mA)
- **YLI YL-99** (12V, 800mA)
- Generic 12V electric strike locks

**Where to buy:**
- Amazon: "12V electric strike lock"
- Security supply stores
- AliExpress: "12V electric strike"

**Price:** $20-50 USD

---

### 6. **Power Supply for Door Lock** ⭐ **REQUIRED**

**Recommended: 12V DC Power Adapter**

**Specifications:**
- **Voltage:** 12V DC (must match lock)
- **Current:** 2A minimum (for reliability, lock uses ~500mA-1A)
- **Connector:** Barrel jack or direct wire
- **Type:** AC-DC adapter (plugs into wall)

**Important:** 
- Must be **DC** (not AC)
- Must match your lock's voltage (12V or 24V)
- Current rating should be 2x the lock's requirement (safety margin)

**Where to buy:**
- Amazon: "12V 2A power adapter DC"
- Electronics stores

**Price:** $8-15 USD

---

## 🔧 **OPTIONAL BUT RECOMMENDED**

### 7. **Breadboard** (For Testing)

**Recommended: Half-size breadboard (400 points)**

**Why:**
- Easy prototyping without soldering
- Test connections before permanent installation
- Reusable

**Price:** $3-5 USD

---

### 8. **Logic Level Converter (If using 5V relay)**

**Recommended: Bi-Directional Logic Level Converter 4-Channel**

**Why needed:**
- ESP32 outputs 3.3V, but 5V relays need 5V signal
- This converter steps up 3.3V → 5V
- Protects ESP32 from 5V input

**Alternative:** Buy a **3.3V relay module** instead (simpler, no converter needed)

**Price:** $2-4 USD

---

### 9. **Status LED** (Optional but useful)

**Recommended: 5mm LED (Red/Green)**

**Why:**
- Visual feedback for lock status
- Red = Locked, Green = Unlocked
- Helps with debugging

**What you need:**
- 1x Red LED
- 1x Green LED
- 2x 220Ω resistors (for LED current limiting)

**Price:** $1-2 USD

---

### 10. **USB Cable** (For Programming ESP32)

**Recommended: USB-A to Micro-USB or USB-C**

**Why:**
- Upload code to ESP32
- Serial debugging
- Power during development

**Specifications:**
- **Type:** Match your ESP32 board (Micro-USB or USB-C)
- **Length:** 1-2 meters
- **Quality:** Data cable (not charge-only)

**Price:** $3-5 USD

---

### 11. **Enclosure Box** (For Permanent Installation)

**Recommended: Weatherproof Junction Box**

**Why:**
- Protects ESP32 and relay from dust/moisture
- Professional installation
- Safety (prevents accidental contact)

**Specifications:**
- **Size:** At least 15cm x 10cm x 5cm
- **Material:** Plastic or metal
- **Mounting:** Wall-mountable
- **IP Rating:** IP65 (weatherproof) recommended

**Price:** $10-20 USD

---

## 📊 **COMPLETE SHOPPING LIST SUMMARY**

### **Minimum Required (Basic Setup):**
| Item | Model/Specs | Quantity | Price (USD) |
|------|-------------|----------|-------------|
| ESP32 DevKit | ESP32-WROOM-32 | 1 | $5-10 |
| Relay Module | 1-Channel 3.3V or 5V | 1 | $2-5 |
| Jumper Wires | Male-to-Female, 20cm | 10-20 | $2-5 |
| Electric Strike Lock | 12V DC, 500mA | 1 | $20-50 |
| Lock Power Supply | 12V, 2A DC | 1 | $8-15 |
| ESP32 Power Supply | 5V, 1A USB adapter | 1 | $3-5 |
| USB Cable | Micro-USB or USB-C | 1 | $3-5 |
| **TOTAL** | | | **$43-95** |

### **Recommended (With Testing Components):**
| Item | Model/Specs | Quantity | Price (USD) |
|------|-------------|----------|-------------|
| All items above | | | $43-95 |
| Breadboard | Half-size, 400 points | 1 | $3-5 |
| Logic Level Converter | 4-Channel (if 5V relay) | 1 | $2-4 |
| Status LEDs | Red + Green + Resistors | 2 LEDs, 2 resistors | $1-2 |
| Enclosure Box | Weatherproof, IP65 | 1 | $10-20 |
| **TOTAL** | | | **$59-126** |

---

## 🔌 **WIRING DIAGRAM**

```
ESP32                    Relay Module              Electric Strike Lock
─────────────────       ───────────────          ────────────────────
GPIO 2 (or any) ───────► IN (Signal)
3.3V ──────────────────► VCC
GND ───────────────────► GND
                                                    
                                    COM ──────────► Lock (+)
                                    NO ───────────► Lock (-)
                                    
12V Power Supply ─────────────────────────────────► Lock (+)
GND ──────────────────────────────────────────────► Lock (-)
```

**Important Notes:**
- ESP32 GPIO pins are 3.3V logic
- Use 3.3V relay OR logic level converter for 5V relay
- Relay COM connects to Lock positive terminal
- Relay NO (Normally Open) connects to Lock negative terminal
- When GPIO goes HIGH → Relay closes → Lock unlocks
- Lock power supply must match lock voltage (12V or 24V)

---

## 🛠️ **INSTALLATION STEPS (After Purchase)**

1. **Test ESP32:**
   - Connect USB cable
   - Upload test code (blink LED)
   - Verify WiFi connection

2. **Test Relay:**
   - Connect ESP32 GPIO → Relay IN
   - Connect ESP32 3.3V → Relay VCC
   - Connect ESP32 GND → Relay GND
   - Upload code to toggle relay
   - Listen for "click" sound when relay activates

3. **Test Lock:**
   - Connect 12V power supply directly to lock
   - Verify lock unlocks when power applied
   - Measure current draw (should be ~500mA-1A)

4. **Full Integration:**
   - Connect ESP32 → Relay → Lock
   - Upload door control code
   - Test with API calls from your server

---

## ⚠️ **IMPORTANT SAFETY NOTES**

1. **High Voltage Warning:**
   - Electric strike locks use 12V-24V DC (relatively safe)
   - But always disconnect power before wiring
   - Double-check connections before powering on

2. **Relay Isolation:**
   - Always use optocoupler relay (isolates ESP32 from lock circuit)
   - Prevents ESP32 damage if lock circuit fails

3. **Power Supply:**
   - Use proper AC-DC adapters (not random chargers)
   - Match voltage exactly (12V lock = 12V supply)
   - Use current rating 2x lock requirement (safety margin)

4. **Wiring:**
   - Use proper wire gauge (18-22 AWG for low voltage)
   - Secure connections (screw terminals or soldering)
   - Avoid loose connections (fire hazard)

5. **Testing:**
   - Test each component separately first
   - Use multimeter to verify voltages
   - Test with low voltage before full power

---

## 🎯 **WHERE TO BUY**

### **Online (Recommended):**
- **Amazon:** Fast shipping, good return policy
- **AliExpress:** Cheaper, longer shipping (2-4 weeks)
- **SparkFun/Adafruit:** Premium quality, higher price
- **DigiKey/Mouser:** Professional components, bulk orders

### **Local Stores:**
- Electronics stores (RadioShack equivalent)
- Security supply stores (for locks)
- Hardware stores (for wiring, enclosures)

---

## 💡 **PRO TIPS**

1. **Buy Extra Components:**
   - Get 2x ESP32 boards (one backup)
   - Get 2x relay modules (one backup)
   - Jumper wires are cheap, get extra

2. **Start Simple:**
   - Test with LED first (instead of lock)
   - Verify ESP32 → Relay works
   - Then add lock

3. **Document Everything:**
   - Take photos of wiring
   - Note which GPIO pins you used
   - Save lock specifications

4. **Future Upgrades:**
   - Add buzzer for audio feedback
   - Add RFID reader for backup access
   - Add door sensor (know if door is open/closed)
   - Add status display (OLED screen)

---

## 📝 **ESP32 CODE REQUIREMENTS**

After buying hardware, you'll need ESP32 code that:
1. Connects to WiFi
2. Listens for HTTP POST requests from your server
3. Parses JSON: `{"authenticated": true/false}`
4. Controls GPIO pin (HIGH = unlock, LOW = lock)
5. Auto-locks after timeout (e.g., 5 seconds)

**Example API Endpoint:**
```
POST http://your-esp32-ip/unlock
Body: {"authenticated": true}
```

---

## ✅ **CHECKLIST BEFORE BUYING**

- [ ] ESP32 board (with WiFi)
- [ ] Relay module (3.3V or 5V + level converter)
- [ ] Jumper wires (10-20 pieces)
- [ ] Electric strike lock (12V or 24V)
- [ ] Lock power supply (matches lock voltage, 2A+)
- [ ] ESP32 power supply (5V, 1A+)
- [ ] USB cable (for programming)
- [ ] Breadboard (for testing)
- [ ] Enclosure box (for permanent install)

---

**Total Estimated Cost: $43-126 USD** (depending on components and quality)

**Ready to order?** Start with the minimum required list, then add optional components as needed!
