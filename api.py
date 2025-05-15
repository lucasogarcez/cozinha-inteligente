# app.py — Servidor Flask
from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Função para conectar ao banco
def conectar():
    return psycopg2.connect(
        dbname="cozinha",
        user="seuuser",
        password="suasenha",
        host="localhost",
        port="5432"
    )

# Rota para receber os dados do ESP32
@app.route('/dados', methods=['POST'])
def receber_dados():
    dados = request.get_json()
    temp = dados['temperatura']
    umi = dados['umidade']
    gas = dados['gas']

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO leituras (temperatura, umidade, gas)
        VALUES (%s, %s, %s)
    """, (temp, umi, gas))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "salvo"})

# Rota para buscar os últimos dados
@app.route('/ultimos-dados')
def ultimos_dados():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT timestamp, temperatura, umidade, gas FROM leituras ORDER BY id DESC LIMIT 20")
    linhas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([
        {"timestamp": str(l[0]), "temperatura": l[1], "umidade": l[2], "gas": l[3]}
        for l in linhas[::-1]  # do mais antigo para o mais recente
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
