# 3. Tech Stack Options & Evaluation Matrix

This document provides an engineering evaluation of three different implementation pathways for the IoT Air Quality & Pollution Monitoring Dashboard. It outlines the components, difficulty levels, expected outputs, and hardware dependencies for each option.

---

## 1. Architectural Options Evaluation

### 🟢 Option A: Basic / Entry-Level Pathway
* **Core Microcontroller:** Arduino UNO (or simulated equivalent).
* **Sensor Logic:** Static mathematical sensor mock loops running inside software.
* **Connectivity:** Purely Local (Serial Monitor output only; no network stack).
* **Target Environment:** Pure simulation environments like Tinkercad.
* **Difficulty Level:** Very Low (Beginner).
* **Hardware Required:** No. Can be done 100% via virtual web sandboxes.
* **Engineering Output:** Simple local text-based warning indicators. No real-time historical tracking, cloud ingestion, or dashboard capabilities.

### 🔵 Option B: Recommended Pathway (Student & Portfolio Focused)
* **Core Microcontroller:** ESP32 System-on-Chip (SoC) with built-in Wi-Fi and Bluetooth.
* **Sensor Integration:** MQ135 Air Quality Sensor + DHT11/DHT22 Temperature and Humidity Sensor.
* **Connectivity Protocol:** HTTP/HTTPS REST API Client.
* **Cloud Infrastructure:** ThingSpeak / Blynk IoT Cloud Platform (Time-series data storage and visualization).
* **Alternative Simulator:** Direct Python 3 Core Environmental Matrix Engine (for non-hardware tracks).
* **Difficulty Level:** Medium (Industry-Relevant yet accessible).
* **Hardware Required:** Optional. Can be completely deployed physically or running via the accompanying local Python analytical framework.
* **Engineering Output:** Real-time multi-field cloud charts, automatic CSV transaction logging, dynamic threshold triggers, and automated web dashboard widgets.

### 🔴 Option C: Advanced / Production-Grade Pathway
* **Core Microcontroller:** ESP32 or Raspberry Pi Pico W.
* **Sensor Integration:** Multiple industrial-grade sensors (MQ135, MQ2, PM2.5 Laser Sensors, $CO_2$ NDIR sensors).
* **Connectivity Protocol:** MQTT (Message Queuing Telemetry Transport) over secure WebSockets.
* **Cloud Infrastructure:** Local Node-RED orchestrator or AWS IoT Core linked to an InfluxDB time-series database and Grafana visualization UI.
* **Difficulty Level:** High (Advanced).
* **Hardware Required:** Highly recommended for optimal sensor calibration arrays.
* **Engineering Output:** Enterprise-ready event broker network, sub-second telemetry updates, deep data storage layers, and highly customizable UI/UX control centers.

---

## 2. Why Option B is Selected for This Project

This project leverages **Option B** as its primary structural architecture. It offers the best engineering compromises for students looking to maximize portfolio impact:

1. **Dual Implementation Capability:** Students lacking access to actual, physical integrated circuits can run the robust local Python simulation framework. Students with physical parts can deploy the matching C++ firmware without changing their underlying cloud structures.
2. **True Cloud Integration:** Using ThingSpeak transforms the project from a localized circuit loop into a genuine IoT network, demonstrating full edge-to-cloud data pipelining to prospective recruiters.
3. **Low Financial / Computational Barrier:** Both the Python runtime environment and the basic ThingSpeak cloud tier are 100% free, removing the need for complex, paid enterprise subscription models.
