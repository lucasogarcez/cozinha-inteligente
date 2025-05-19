//Cozinha inteligente WEB-API-Backend

#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#include "secrets.h" // Contém WIFI_SSID, WIFI_PASSWORD, SERVER_URL

#define DHTPIN 4     // Pino onde o DHT está conectado
#define DHTTYPE DHT11 // Tipo do sensor DHT (DHT11 ou DHT22)
#define GAS_SENSOR_PIN 34 // Pino do sensor de gás

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }
  Serial.println("Conectado!");
}

void loop() {
  float temperatura = dht.readTemperature();
  float umidade = dht.readHumidity();
  float gas = analogRead(GAS_SENSOR_PIN);

  // Verifica se a leitura falhou
  if (isnan(temperatura) || isnan(umidade)) {
    Serial.println("Falha ao ler do DHT!");
    delay(5000);
    return;
  }

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(SERVER_URL); // URL vinda do secrets.h
    http.addHeader("Content-Type", "application/json");

    String json = "{\"temperatura\": " + String(temperatura, 1) + ", \"umidade\": " + String(umidade, 1) + ", \"gas\": " + String(gas) + "}";

    // Envia os dados para o servidor
    int resposta = http.POST(json);
    Serial.println("Enviando dados: " + json);
    Serial.println("Resposta: " + String(resposta));
    http.end();
  } else {
    Serial.println("WiFi desconectado.");
  }
  delay(10000); // Espera 10 segundos antes de enviar de novo
}
