# IoT-Based Air Quality & Pollution Monitoring Network

An enterprise-inspired, Edge-to-Cloud Internet of Things (IoT) network architecture designed to measure environmental and toxic gas metrics in real time. This repository implements a dual-mode workflow featuring production-grade **C++ ESP32 microchip firmware** and an autonomous **Python-driven data pipeline simulator** that pipes telemetry data directly to a cloud analytical dashboard.

---

## 🚀 Key Features & Architectural Capabilities
* **Dual-Track Framework:** Supports actual physical hardware deployment (ESP32) and local virtual execution (Python) seamlessly.
* **Multi-Sensor Acquisition Loop:** Collects simultaneous telemetry for Gas Concentrations (PPM), Temperature (°C), and Humidity (%).
* **Edge Analytics Engine:** Classifies ambient air indices locally into four dynamic categories: *Good, Moderate, Poor, and Hazardous*.
* **Local Hardware Interrupts:** Coordinates physical audio buzzer modulations and visual status LED warning alerts.
* **Time-Series Cloud Logging:** Integrates with ThingSpeak Cloud via a secure HTTP API interface for historical charting.
* **Local Persistent Database:** Logs transactional historical data straight to disk inside an audit-ready `sensor_logs.csv` ledger.
* **Central Master Entry Hub:** Houses a single console-menu workspace script (`main.py`) to orchestrate live tracking or generate custom high-resolution chart assets automatically.

---

## 📁 Repository Directory Architecture

```text
IoT-Air-Quality-Pollution-Dashboard/
│
├── arduino_code/
│   └── arduino_code.ino       # Production-grade C++ ESP32 Edge Firmware
│
├── python_simulation/
│   └── simulation.py          # Autonomous multi-scenario environmental data matrix generator
│
├── docs/
│   ├── project_explanation.md  # Deep technical operational review & problem statements
│   ├── industry_relevance.md   # Practical breakdown of cross-sector industrial deployments
│   ├── tech_stack.md           # Evaluation matrix comparing architectural options
│   └── circuit_diagram.md      # Pin-map connection registries & hardware engineering rules
│
├── data/
│   └── sensor_logs.csv        # Local persistent time-series database (Git-ignored)
│
├── outputs/
│   └── air_quality_trends.png # Exported analytical trends charts (Git-ignored)
│
├── reports/
│   └── sample_air_quality_report.txt # Auto-compiled environmental metrics compliance audit log
│
├── main.py                    # Master system central entry point control hub
├── requirements.txt           # Explicit Python environment configuration checklist
└── .gitignore                 # Workspace isolation matrix preventing key leaks
```

---

## 🛠️ Step-by-Step Setup & Local Execution Guide

### 1. Configure the Cloud Analytics Dashboard
1. Set up a free account at [ThingSpeak Cloud Ingestion Platform](https://thingspeak.com).
2. Create a **New Channel** titled `Air Quality Dashboard Network`.
3. Activate exactly four tracking fields:
   * **Field 1:** Gas Density (PPM / ADC)
   * **Field 2:** Ambient Temperature (°C)
   * **Field 3:** Relative Humidity (%)
   * **Field 4:** Health Status Code (1-4)
4. Navigate to the **API Keys** panel and copy your private **Write API Key**.
5. Paste your key into your active script configuration line (`simulation.py` for virtual execution or `arduino_code.ino` for hardware setups).

### 2. Launch the Software Virtual Tracking Suite
Open your preferred terminal profile inside the workspace and run the following commands:

```bash
# Verify local environment packages match production rules
pip install -r requirements.txt

# Execute the project master entry point control hub
python main.py
```

#### Running Options:
* Select **`1`** from the terminal menu to ignite the live sensor simulation loop. Watch it rotate through changing scenarios and sync telemetry packages remotely every 15 seconds. Press `Ctrl + C` to return to the hub menu.
* Select **`2`** from the terminal menu to process the stored historical logs. This compiles a text audit report inside `reports/` and exports a high-resolution trends graph to `outputs/`.

---

Project Facts
Market Growth 📈
 The global air quality monitoring market is expected to reach USD 9.7 billion by 2030, driven by IoT-based smart city initiatives.
Cost Savings 💰
 Low-cost IoT sensors reduce deployment costs by 70 % compared to industrial monitoring stations, allowing dense environmental mapping.
Equipment Longevity ⚙️
 Proper filtration and periodic calibration extend sensor life beyond 18 months in outdoor environments.
Real-World Applications 🌍
Smart City Air Monitoring (e.g., Pune, Delhi, Singapore).


Industrial emissions control and workplace safety.


School and hospital air monitoring for health compliance.


Environmental research and student projects.


Industry Adoption 🏭
 Used by Bosch Air Quality, Siemens Smart City, Honeywell Analytics, and Indian NCAP Labs for low-cost urban AQI mapping.
Interview Question and Answer

-- 1. Interview Question: Explain your IoT-Based Air Quality & Pollution Monitoring Dashboard project.
-- Answer:
-- In this project, I built an IoT-based air quality monitoring system that measures pollution-related values using sensors such as MQ135 and environmental values like temperature and humidity using DHT11 or DHT22. The system processes sensor readings, classifies air quality as Good, Moderate, Poor, or Hazardous, generates alerts when pollution crosses a threshold, and displays the data on a dashboard. This project demonstrates IoT concepts like sensor data collection, microcontroller processing, cloud dashboard integration, alert generation, and environmental monitoring.

-- 2. Interview Question: What problem does this project solve?
-- Answer:
-- This project solves the problem of monitoring air pollution manually. It helps users track air quality in real time and receive alerts when pollution levels become unsafe.

-- 3. Interview Question: Which sensors are used in this project?
-- Answer:
-- This project can use an MQ135 sensor for air quality detection, MQ2 sensor for smoke or gas detection, and DHT11 or DHT22 sensor for temperature and humidity monitoring.

-- 4. Interview Question: Which microcontroller can be used?
-- Answer:
-- ESP32 is recommended because it has built-in Wi-Fi, which makes it easy to send sensor data to a cloud dashboard. Arduino UNO can also be used for a basic version, but it may require an extra Wi-Fi module.

-- 5. Interview Question: How does the air quality alert system work?
-- Answer:
-- The system reads pollution sensor values and compares them with predefined threshold levels. If the value crosses the safe limit, the system triggers an alert using buzzer, LED, dashboard notification, or message output.

-- 6. Interview Question: How is IoT used in this project?
-- Answer:
-- IoT is used by collecting air quality data from sensors and sending it to a cloud dashboard where users can monitor pollution levels remotely in real time.

-- 7. Interview Question: What output does the project generate?
-- Answer:
-- The project generates air quality values, temperature, humidity, pollution category, alert status, dashboard graphs, and CSV logs for historical analysis.

-- 8. Interview Question: Why is data logging important in this project?
-- Answer:
-- Data logging helps store pollution readings over time. This allows users to analyze air quality trends, compare pollution levels, and identify unsafe periods.

-- 9. Interview Question: What challenges did you face in this project?
-- Answer:
-- The main challenges were setting correct threshold values, handling fluctuating sensor readings, simulating realistic pollution data, integrating dashboard updates, and avoiding false alerts.

-- 10. Interview Question: How can this project be improved further?
-- Answer:
-- This project can be improved by adding multiple gas sensors, GPS-based pollution mapping, mobile app alerts, AQI calculation using standard formulas, AI-based pollution prediction, solar-powered deployment, and real-time city-level dashboard integration.


