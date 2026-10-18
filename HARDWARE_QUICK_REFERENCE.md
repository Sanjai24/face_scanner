# ⚡ ESP32 Hardware Quick Reference

## 🎯 **ESSENTIAL MODELS TO BUY**

### 1. **ESP32 Board**
**Model:** `ESP32-DevKitC-32E` or `ESP32-WROOM-32`
- Built-in WiFi + Bluetooth
- 30+ GPIO pins
- USB-C or Micro-USB
- **Price:** $5-10

### 2. **Relay Module**
**Model:** `1-Channel 3.3V Relay Module` (with optocoupler)
- OR: `1-Channel 5V Relay Module` + Logic Level Converter
- **Price:** $2-5

### 3. **Electric Strike Lock**
**Model:** `12V DC Electric Strike Lock` (Fail-Safe)
- Current: 500mA-1A
- **Price:** $20-50

### 4. **Power Supplies**
- **ESP32:** 5V, 1A USB adapter ($3-5)
- **Lock:** 12V, 2A DC adapter ($8-15)

### 5. **Jumper Wires**
- Male-to-Female, 20cm, 10-20 pieces ($2-5)

---

## 💰 **TOTAL COST: $40-95 USD**

---

## 🔌 **QUICK WIRING**

```
ESP32 GPIO 2 ──► Relay IN
ESP32 3.3V  ──► Relay VCC
ESP32 GND   ──► Relay GND

Relay COM ──► Lock (+)
Relay NO  ──► Lock (-)

12V Supply ──► Lock (+)
GND        ──► Lock (-)
```

---

## 📦 **WHERE TO BUY**

- **Amazon:** Fast shipping
- **AliExpress:** Cheaper, slower
- **SparkFun/Adafruit:** Premium quality

---

**See `HARDWARE_SHOPPING_LIST.md` for complete details!**
