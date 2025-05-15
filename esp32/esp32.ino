//Cozinha inteligente WEB-API-Backend

#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "SUA_REDE";
const char* senha = "SUA_SENHA";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, senha);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }
  Serial.println("Conectado!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin("http://SEU_IP:5000/dados"); // Substitua pelo IP do seu servidor Flask
    http.addHeader("Content-Type", "application/json");

    String json = "{\"temperatura\": 28.5, \"umidade\": 60, \"gas\": 350}";
    int resposta = http.POST(json);

    Serial.println("Resposta: " + String(resposta));
    http.end();
  }
  delay(10000);
}
