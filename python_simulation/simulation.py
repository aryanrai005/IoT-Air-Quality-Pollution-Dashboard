import time
import random
import csv
import os
from datetime import datetime
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

# ==============================================================================
# --- CONFIGURATION ENGINE ---
# ==============================================================================
# Change this to your actual ThingSpeak Write API Key once your dashboard is set up.
# If left as default, the script will smoothly run in offline/local simulation mode.
THINGSPEAK_API_KEY = "YOUR_THINGSPEAK_WRITE_KEY" 
THINGSPEAK_URL = "https://thingspeak.com"
CSV_FILE_PATH = "data/sensor_logs.csv"

# Ensure target data directory exists cleanly
os.makedirs("data", exist_ok=True)

def calculate_aqi_category(ppm):
    """
    Classifies air quality based on industry standard PPM/AQI thresholds
    and assigns local visual/audible alert patterns.
    """
    if ppm < 150:
        return "Good", "Normal Atmospheric Air. System Safe.", 1
    elif ppm < 300:
        return "Moderate", "Acceptable. Increased ventilation recommended.", 2
    elif ppm < 700:
        return "Poor", "[ALERT] Buzzer Beeping! Visual Red LED Active.", 3
    else:
        return "Hazardous", "[CRITICAL] Alarm Sounding! Evacuate / Ventilate Area!", 4

def send_to_cloud_dashboard(ppm, temp, hum, status_code):
    """
    Handles outbound synchronization to the remote cloud ingestion server via HTTP.
    """
    if THINGSPEAK_API_KEY == "YOUR_THINGSPEAK_WRITE_KEY" or THINGSPEAK_API_KEY == "":
        return "Cloud Sync: Skipped (Using Local-Only Evaluation Mode)"

    payload = {
        "api_key": THINGSPEAK_API_KEY,
        "field1": ppm,
        "field2": temp,
        "field3": hum,
        "field4": status_code
    }
    query = urlencode(payload)
    url = f"{THINGSPEAK_URL}/update?{query}"
    try:
        with urlopen(url, timeout=5) as response:
            status_code = response.getcode()
            if status_code == 200:
                return "Cloud Sync: Success (Telemetry Pushed)"
            return f"Cloud Sync: Failed (HTTP Error {status_code})"
    except URLError:
        return "Cloud Sync: Network Timeout / Offline Mode Active"

def log_to_csv_database(timestamp, ppm, temp, hum, category, alert_text):
    """
    Maintains a local persistent time-series transaction registry for audits.
    """
    file_exists = os.path.isfile(CSV_FILE_PATH)
    with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            # Write structured relational headers on database creation
            writer.writerow(["Timestamp", "Air_Quality_PPM", "Temperature_C", "Humidity_Pct", "Air_Category", "Alert_Status"])
        writer.writerow([timestamp, ppm, temp, hum, category, alert_text])

# ==============================================================================
# --- MAIN ARDUINO-STYLE EXECUTION LOOP ---
# ==============================================================================
print("=================================================================")
print("  IoT AIR QUALITY & POLLUTION DASHBOARD VIRTUAL CORE SIMULATOR   ")
print("=================================================================")
print(f"Tracking local telemetry and logging instances to: {CSV_FILE_PATH}")
print("Simulating changing environmental cycles... Press Ctrl+C to safely exit.\n")

try:
    cycle_step = 0
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cycle_step += 1
        
        # Environmental Profile Simulation Engine (Simulates real-world daily variations)
        if cycle_step <= 4:    
            # SCENARIO 1: Clean baseline conditions (e.g., Early morning, active HVAC filtration)
            ppm = random.randint(70, 145)
            temp = round(random.uniform(21.0, 24.5), 1)
            hum = round(random.uniform(40.0, 48.0), 1)
        elif cycle_step <= 8:  
            # SCENARIO 2: Gradual deterioration (e.g., Stale indoor air, closed windows, human traffic)
            ppm = random.randint(160, 295)
            temp = round(random.uniform(25.0, 28.2), 1)
            hum = round(random.uniform(50.0, 58.0), 1)
        elif cycle_step <= 12: 
            # SCENARIO 3: Sudden Industrial Outflow / Heavy Kitchen Smoke Spike
            ppm = random.randint(750, 1150)
            temp = round(random.uniform(31.0, 36.5), 1)
            hum = round(random.uniform(22.0, 34.0), 1)
        else:            
            # Reset timeline cycle to run indefinitely
            cycle_step = 0
            continue

        # Evaluate and process metrics locally
        category, alert_msg, status_code = calculate_aqi_category(ppm)
        
        # Persist transactions locally to disk
        log_to_csv_database(timestamp, ppm, temp, hum, category, alert_msg)
        
        # Dispatch telemetry payloads outbound to ThingSpeak interface
        cloud_network_status = send_to_cloud_dashboard(ppm, temp, hum, status_code)

        # Print clean, human-readable terminal dashboard outputs
        print(f"[{timestamp}] Metrics Checked")
        print(f" -> Sensors: Gas Conc: {ppm} PPM | Temp: {temp}°C | Humid: {hum}%")
        print(f" -> Analytics: Category: {category} | Action Required: {alert_msg}")
        print(f" -> Network: {cloud_network_status}")
        print("-" * 65)

        # ThingSpeak open public API channels limit telemetry reception to 1 update every 15 seconds
        time.sleep(15)

except KeyboardInterrupt:
    print("\n[INFO] Simulation terminated by operator safely. Clean terminal handle released.")
