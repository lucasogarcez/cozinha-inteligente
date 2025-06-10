//Cozinha inteligente WEB-API-Backend

#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#include "secrets.h" // Contém WIFI_SSID, WIFI_PASSWORD, SERVER_URL

#define DHTPIN 14     // Pino onde o DHT está conectado
#define DHTTYPE DHT11 // Tipo do sensor DHT (DHT11 ou DHT22)
#define GAS_SENSOR_PIN 34 // Pino do sensor de gás

DHT dht(DHTPIN, DHTTYPE);

// Atuadores
#define BUZZER_PIN 13
#define COOLER_PIN_LIGA 15 //IN1
#define COOLER_PIN_DESLIGA 2 //IN2
#define LED_PIN 12

void setup() {
  Serial.begin(115200);
  // Inicializa o DHT
  dht.begin();

  // Inicializa os atuadores
  ppinMode(BUZZER_PIN, OUTPUT);
  pinMode(COOLER_PIN_LIGA, OUTPUT);
  pinMode(COOLER_PIN_DESLIGA, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  // Conecta o módulo ao WiFi
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

  if (isnan(gas)) {
    Serial.println("Falha ao ler do sensor de gás!");
    delay(5000);
    return;
  }

  // Verifica condições de acionamento dos atuadores
  bool alarme = false;

  // Situação crítica: gás muito alto → Jogar ar para fora
  if (gas >= 2100 || temperatura >= 30) {
    digitalWrite(COOLER_PIN_LIGA, HIGH);
    digitalWrite(COOLER_PIN_DESLIGA, LOW);
    alarme = true;
  } else { // Situação estável: desligar tudo
      digitalWrite(COOLER_PIN_LIGA, LOW);
      digitalWrite(COOLER_PIN_DESLIGA, LOW);
  }

  // Buzzer: ligado se algum risco detectado
  digitalWrite(BUZZER_PIN, alarme ? HIGH : LOW);
  digitalWrite(LED_PIN, alarme ? HIGH : LOW);

  // Inicializa o servidor
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(SERVER_URL); // URL vinda do secrets.h
    http.addHeader("Content-Type", "application/json");

    String json = "{\"temperatura\": " + String(temperatura, 1) + ", \"umidade\": " + String(umidade, 1) + ", \"gas\": " + String(gas, 1) + "}";

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
