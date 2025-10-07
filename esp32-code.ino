#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"
#include <ArduinoJson.h>

#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define MQ135PIN 34
#define RELAYPIN 2

const char* ssid = "Pixel 6 Pro";
const char* password = "01_ALPHA";

const char* serverPost = "http://10.157.126.30:5000/post_data";

void setup() {
  Serial.begin(115200);
  pinMode(RELAYPIN, OUTPUT);
  digitalWrite(RELAYPIN, LOW);
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  dht.begin();
}

void loop() {
  delay(5000);

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int airAnalog = analogRead(MQ135PIN);
  int airQuality = airAnalog; // raw value for simplicity

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read DHT sensor!");
    return;
  }

  String jsonData = "{\"temperature\": " + String(temperature) +
                    ", \"humidity\": " + String(humidity) +
                    ", \"AQI\": \"" + airQuality + "\"}";

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverPost);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Server response: " + response);

      DynamicJsonDocument doc(200);
      DeserializationError error = deserializeJson(doc, response);

      if (!error) {
        if (doc["toggle"] == 1) {
          digitalWrite(RELAYPIN, HIGH);
          Serial.println("Fan: ON");
        } else {
          digitalWrite(RELAYPIN, LOW);
          Serial.println("Fan: OFF");
        }
      } else {
        Serial.println("Failed to parse JSON from server");
      }

    } else {
      Serial.print("Error sending data: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }
}


// #define RELAYPIN 4  // Relay connected to D2

// void setup() {
//   Serial.begin(115200);
//   pinMode(RELAYPIN, OUTPUT);
//   digitalWrite(RELAYPIN, LOW);  // Start with relay OFF
// }

// void loop() {
//   // Turn relay ON
//   digitalWrite(RELAYPIN, HIGH);
//   Serial.println("Relay ON");
//   delay(2000);  // Wait 2 seconds

//   // Turn relay OFF
//   digitalWrite(RELAYPIN, LOW);
//   Serial.println("Relay OFF");
//   delay(2000);  // Wait 2 seconds
// }

