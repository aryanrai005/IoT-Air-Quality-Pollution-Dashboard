# 4. Hardware Wiring Configuration & Circuit Matrix

This document details the physical electrical wiring layout between the core ESP32 microchip microcontroller and the sensory/actuator peripheral cluster. Use this data matrix as a reference guide for circuit troubleshooting and breadboard routing.

---

## 1. Master System Wiring Matrix

| Peripheral Component | Pin Label on Component | Target Destination Pin on ESP32 | Electrical Protocol / Signal Type | Purpose / Description |
| :--- | :--- | :--- | :--- | :--- |
| **MQ135 Gas Sensor** | VCC | 5V / VIN | Power Line (5V DC) | Provides heating element activation voltage. |
| | GND | GND | Ground Reference | Common ground link. |
| | AO (Analog Out) | GPIO 34 (ADC1_CH6) | Analog Signal (0 - 3.3V) | Delivers raw continuous sensory voltage mapping. |
| | DO (Digital Out) | *Unconnected* | Not Used | Secondary digital threshold latch (unused). |
| **DHT11 Temp/Hum** | VCC | 3V3 | Power Line (3.3V DC) | Powers sensory digital circuit module. |
| | GND | GND | Ground Reference | Common ground link. |
| | DATA / OUT | GPIO 4 | Digital Single-Bus Stream | Chronological bidirectional environmental telemetry. |
| **Piezo Buzzer** | Positive (+) Line | GPIO 25 (DAC1) | Digital Logic Output | Triggers audio frequencies on critical air thresholds. |
| | Negative (-) Line | GND | Ground Reference | Ground return path. |
| **Status LED: RED** | Long Pin (Anode +) | GPIO 26 | Digital Logic Output (via Resistor) | Visual warning indicator for poor/hazardous air. |
| | Short Pin (Cathode -)| GND | Ground Reference | Ground return through common bus line. |
| **Status LED: GREEN**| Long Pin (Anode +) | GPIO 27 | Digital Logic Output (via Resistor) | Visual normal system verification baseline status. |
| | Short Pin (Cathode -)| GND | Ground Reference | Ground return through common bus line. |

---

## 2. Mandatory Electrical Engineering Notes

### 💡 Current Limiting In-Line Resistors
* **Warning:** Never connect the positive lines of the Red and Green LEDs directly to the ESP32 GPIO channels without protection. 
* **Correction:** You MUST solder or slot an in-line **220Ω to 330Ω resistor** between the GPIO output pins (GPIO 26 and 27) and the positive leg (Anode) of each LED. This drops voltage overhead safely and prevents burning out the internal microcontroller output transistors.

### 🔋 Power Allocation Interlocks
* The MQ135 gas sensor contains an internal chemical heating element that draws substantial baseline current (~150mA). 
* **Rule:** If your laptop USB rail droops or errors out during multi-sensor reading cycles, isolate the MQ135 sensor onto an independent, external 5V power source, keeping the ground reference lines shared.

### 🔌 Microcontroller ADC Input Constraints
* The ESP32 Analog-to-Digital Converter (ADC) channels are natively non-linear and read up to a hardware limit of 3.3V. 
* While the MQ135 can run its logic safely at 5V, verify your specific breakout sensor board utilizes a voltage division network outputting a max 3.3V threshold signature to avoid degrading the raw input integrity of GPIO 34 over time.
