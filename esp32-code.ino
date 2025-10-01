#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"
#include <ArduinoJson.h>  // Include ArduinoJson library for parsing JSON

// ---------- Pin definitions ----------
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define MQ135PIN 34    // Analog pin for air quality sensor
#define RELAYPIN 2     // Relay to control fan

// ---------- WiFi credentials ----------
const char* ssid = "Pixel 6 Pro";
const char* password = "01_ALPHA";

// ---------- Flask server endpoints ----------
const char* serverPost = "http://192.168.29.119:5000/post_data";
const char* serverGet  = "http://192.168.29.119:5000/get_data";

float threshold = 27.0;   // Default temperature threshold
bool manualToggle = false;

void setup() {
  Serial.begin(115200);

  // Relay setup
  pinMode(RELAYPIN, OUTPUT);
  digitalWrite(RELAYPIN, LOW); // Fan off initially

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");

  // Initialize DHT sensor
  dht.begin();
}

void loop() {
  delay(5000);  // Wait 5 seconds between reads

  // --- Read sensors ---
  float temperature = dht.readTemperature();
  float humidity    = dht.readHumidity();
  int airAnalog     = analogRead(MQ135PIN); // 0-4095
  String airQuality = getAQI(airAnalog);

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read DHT sensor!");
    return;
  }

  // --- Prepare JSON data ---
  String jsonData = "{\"temperature\": " + String(temperature) +
                    ", \"humidity\": " + String(humidity) +
                    ", \"AQI\": \"" + airQuality + "\"}";

  // --- Send data to Flask server ---
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverPost);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("Server response: ");
      Serial.println(response);

      // --- Parse JSON response ---
      DynamicJsonDocument doc(200);
      DeserializationError error = deserializeJson(doc, response);

      if (!error) {
        int toggleState = doc["toggle"] | 0; // Default 0 if not present

        // --- Relay control logic ---
        if (!manualToggle) {  // Only auto-toggle if manual not active
          if (temperature > threshold) {
            digitalWrite(RELAYPIN, HIGH);
          } else {
            digitalWrite(RELAYPIN, LOW);
          }
        } else {
          // Keep relay state as per manual toggle
          if (toggleState == 1) digitalWrite(RELAYPIN, HIGH);
          else digitalWrite(RELAYPIN, LOW);
        }
      } else {
        Serial.println("Failed to parse JSON from server response");
      }

    } else {
      Serial.print("Error sending data: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }
}

// --- Convert MQ135 analog reading to AQI description ---
String getAQI(int val) {
  if (val < 1024) return "Good";
  else if (val < 2048) return "Moderate";
  else if (val < 3072) return "Unhealthy for Sensitive Groups";
  else if (val < 3584) return "Unhealthy";
  else if (val < 3840) return "Very Unhealthy";
  else return "Hazardous";
}