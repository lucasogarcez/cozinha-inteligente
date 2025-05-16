//Cozinha inteligente WEB-API-Backend

#include <WiFi.h>
#include <HTTPClient.h>

#include "secrets.h" // Arquivo com dados de WIFI e URL

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }
  Serial.println("Conectado!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");

    String json = "{\"temperatura\": 28.5, \"umidade\": 60, \"gas\": 350}";
    int resposta = http.POST(json);

    Serial.println("Resposta: " + String(resposta));
    http.end();
  }
  delay(10000);
}
