CREATE DATABASE cozinha_inteligente;

CREATE TABLE leituras (
	id SERIAL PRIMARY KEY,
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	temperatura REAL,
	umidade REAL,
	gas INTEGER
);