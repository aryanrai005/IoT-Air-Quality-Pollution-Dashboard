#include <WiFi.h>
#include <DHT.h>
#include "ThingSpeak.h"

// ==============================================================================
// --- HARDWARE CONFIGURATION & PIN MAPS ---
// ==============================================================================
#define DHTPIN 4          // DHT11/DHT22 Data Line connected to GPIO 4
#define DHTTYPE DHT11     // Change to DHT22 if using that specific variant
#define MQ135_PIN 34      // MQ135 Analog Output linked to ADC1 Pin GPIO 34
#define BUZZER_PIN 25     // Active/Passive Alarm Buzzer on GPIO 25
#define LED_RED_PIN 26    // Warning Indicator LED on GPIO 26
#define LED_GREEN_PIN 27  // Safe Condition Indicator LED on GPIO 27

// --- NETWORK CREDENTIALS ---
// Replace with your active local router details
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// --- CLOUD DASHBOARD PROPERTIES ---
// Replace with your actual ThingSpeak infrastructure keys
unsigned long CHANNEL_ID = 2400000;         
const char* WRITE_API_KEY = "YOUR_WRITE_API_KEY"; 

// --- INSTANCE INITIALIZATION ---
WiFiClient networkClient;
DHT dhtSensor(DHTPIN, DHTTYPE);

// ==============================================================================
// --- SYSTEM SETUP ENGINE ---
// ==============================================================================
void setup() {
    // Initialize Hardware Serial Monitor for terminal tracking
    Serial.begin(115200);
    delay(10) ;
    
    // Configure Peripheral Output Pins
    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(LED_RED_PIN, OUTPUT);
    pinMode(LED_GREEN_PIN, OUTPUT);
    
    // Default boot pin state: Indicators OFF
    digitalWrite(BUZZER_PIN, LOW);
    digitalWrite(LED_RED_PIN, LOW);
    digitalWrite(LED_GREEN_PIN, LOW);
    
    // Wake up environmental sensors
    dhtSensor.begin();
    
    // Establish Network Connection Link
    Serial.println("\n=============================================");
    Serial.print("Initializing System Wi-Fi Interface Connection");
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    
    int connectionTimeout = 0;
    while (WiFi.status() != WL_CONNECTED && connectionTimeout < 30) {
        delay(500);
        Serial.print(".");
        connectionTimeout++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\n[SUCCESS] Local Wi-Fi Connection Established!");
        Serial.print("Local IP Endpoint: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println("\n[WARNING] Wi-Fi Connection Timeout. Running in Offline Mode.");
    }
    
    // Link ThingSpeak Ingestion Client
    ThingSpeak.begin(networkClient);
    Serial.println("System Core Boot Cycle Finished Cleanly.");
    Serial.println("=============================================");
}

// ==============================================================================
// --- CORE EXECUTION LOOP ---
// ==============================================================================
void loop() {
    // 1. Data Acquisition Phase
    float temperature_C = dhtSensor.readTemperature();
    float humidity_Pct = dhtSensor.readHumidity();
    int raw_gas_adc = analogRead(MQ135_PIN); // Samples voltage (0 to 4095 on ESP32)
    
    // Hardware Line Safety Verification Interlock
    if (isnan(temperature_C) || isnan(humidity_Pct)) {
        Serial.println("[ERROR] Failed to query data from DHT sensor lines. Inspect physical wiring connections.");
        delay(3000);
        return;
    }
    
    // Print Local Logs to the Terminal Monitor Interface
    Serial.print("[" + String(millis() / 1000) + "s] Readouts -> ");
    Serial.print("Gas ADC: "); Serial.print(raw_gas_adc);
    Serial.print(" | Temp: "); Serial.print(temperature_C, 1);
    Serial.print(" C | Humid: "); Serial.print(humidity_Pct, 1);
    Serial.println("%");

    int current_status_code = 1; // 1 = Good, 2 = Moderate, 3 = Poor, 4 = Hazardous

    // 2. Real-Time Analytics & Local Threshold Engine
    if (raw_gas_adc > 2500) { 
        // SCENARIO: Critical Hazardous Gas Leakage Observed
        current_status_code = 4;
        Serial.println(" -> Category: HAZARDOUS! [CRITICAL ALARM STATUS ACTIVE]");
        digitalWrite(LED_RED_PIN, HIGH);
        digitalWrite(LED_GREEN_PIN, LOW);
        
        // Execute rapid alarm oscillation pulse pattern
        digitalWrite(BUZZER_PIN, HIGH); delay(100);
        digitalWrite(BUZZER_PIN, LOW); delay(100);
        digitalWrite(BUZZER_PIN, HIGH); delay(100);
        digitalWrite(BUZZER_PIN, LOW);
    } 
    else if (raw_gas_adc > 1200) { 
        // SCENARIO: Deteriorating / Poor Air Environment
        current_status_code = 3;
        Serial.println(" -> Category: POOR. [BUZZER WARNING ALERT ACTIVE]");
        digitalWrite(LED_RED_PIN, HIGH);
        digitalWrite(LED_GREEN_PIN, LOW);
        
        // Steady slow warning chime
        digitalWrite(BUZZER_PIN, HIGH); delay(400);
        digitalWrite(BUZZER_PIN, LOW);
    } 
    else if (raw_gas_adc > 600) { 
        // SCENARIO: Moderate Baseline Level Shift
        current_status_code = 2;
        Serial.println(" -> Category: MODERATE. Elevated levels, monitor ventilation.");
        digitalWrite(LED_RED_PIN, HIGH);
        digitalWrite(LED_GREEN_PIN, HIGH); // Both lights active indicate transition state
        digitalWrite(BUZZER_PIN, LOW);
    } 
    else { 
        // SCENARIO: Baseline Normal Atmospheric Health
        current_status_code = 1;
        Serial.println(" -> Category: GOOD. Local atmospheric parameters stable.");
        digitalWrite(LED_RED_PIN, LOW);
        digitalWrite(LED_GREEN_PIN, HIGH);
        digitalWrite(BUZZER_PIN, LOW);
    }

    // 3. Remote Cloud Synchronization Pipeline
    if (WiFi.status() == WL_CONNECTED) {
        ThingSpeak.setField(1, raw_gas_adc);
        ThingSpeak.setField(2, temperature_C);
        ThingSpeak.setField(3, humidity_Pct);
        ThingSpeak.setField(4, current_status_code);
        
        int networkTransmissionStatus = ThingSpeak.writeFields(CHANNEL_ID, WRITE_API_KEY);
        if (networkTransmissionStatus == 200) {
            Serial.println(" -> Cloud Network Status: Telemetry successfully synchronized.");
        } else {
            Serial.println(" -> Cloud Network Status: Transmission failure. Error Code: " + String(networkTransmissionStatus));
        }
    } else {
        Serial.println(" -> Cloud Network Status: Offline Mode Active. Skipping sync step.");
    }
    
    Serial.println("-----------------------------------------------------------------");
    
    // ThingSpeak public instance throttling requires a minimum 15-second delay between inputs
    delay(15000); 
}
