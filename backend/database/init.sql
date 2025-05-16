CREATE DATABASE cozinha_inteligente;

CREATE TABLE leituras (
	id SERIAL PRIMARY KEY,
	data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	temperatura REAL,
	umidade REAL,
	gas_ppm REAL
);