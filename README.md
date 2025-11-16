# 🛜 IOT - ESP32 Air-Quality + DHT11 & Fan Controller

> "An IoT project that reads temperature, humidity (DHT11) and air quality (MQ-135) from an ESP32, posts JSON readings to a Flask server, and receives a `toggle` command back to switch a fan (relay/MOSFET). Includes a small Flask backend (server.py) with endpoints to receive data, expose the latest readings, and set a temperature threshold to control the fan. A frontend (HTML/CSS/JS) is also used to view readings and change threshold."
--

## Details

### ESP32 reads:

- Temperature (DHT11)

- Humidity (DHT11)

- Raw MQ-135 analog value (AQI as raw value)

- ESP32 posts JSON to Flask server every 5 seconds

- Flask server stores latest sensor data and computes toggle (fan ON/OFF) based on a threshold

### Server endpoints:

- POST /post_data — receive sensor data, respond with toggle

- GET /get_data — return latest sensor readings

- POST /set_threshold — set temperature threshold (special values supported)

- Frontend to view data and set threshold (uses index.html, script.js, style.css)

---

## Quick status / behavior summary

- Threshold special values:

  - -1 → Always ON (fan forced ON)

  - 100 → Always OFF (fan forced OFF)

  - any other number → fan ON if temperature > threshold, else OFF


## 🪫Hardware (parts)

- ESP32 devboard (ESP32-WROOM-32)

- DHT11 sensor module

- MQ-135 gas sensor

- Relay module or MOSFET (to drive fan)

- DC fan (typical PC fan: 5V or 12V)

- Wires, breadboard, power supply, common ground

## 🔧 Wiring / Pin mapping 

### ESP32 pins (from esp32.ino):

- DHTPIN -> `GPIO 4` (DHT11 data pin)

- MQ135PIN -> `GPIO 34` (ADC input; analogRead)

- RELAYPIN -> `GPIO 2` (digital output to control relay/MOSFET)
