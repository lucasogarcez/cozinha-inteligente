from flask import Flask, render_template, jsonify, request
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis do arquivo .env

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configurações do banco
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'dbname': os.getenv('DB_NAME'), 
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

# Função para conectar ao banco de dados
def conectar_db():
    return psycopg.connect(**db_config, row_factory=dict_row)

@app.route('/api/dados')
def get_data():
    conn = None # Inicializa conn para garantir que esteja definido
    try:
        conn = conectar_db()
        cur = conn.cursor()

        # Busca os últimos 10 registros
        cur.execute("""
            SELECT data_hora, temperatura, umidade, gas_ppm
            FROM sensores
            ORDER BY data_hora DESC
            LIMIT 10
        """)
        registros = cur.fetchall()
        cur.close()

        # Prepara os dados para o gráfico
        registros.reverse()  # Do mais antigo pro mais novo
        dados = {
            "labels": [r['data_hora'].strftime('%H:%M:%S') for r in registros],
            "temperatura": [r['temperatura'] for r in registros],
            "umidade": [r['umidade'] for r in registros],
            "gas": [r['gas_ppm'] for r in registros]
        }
        return jsonify(dados)
    except Exception as e:
        print(f"Erro ao buscar dados: {e}") # Imprime o erro para depuração
        return jsonify({"status": "error", "message": "Erro ao buscar dados"}), 500
    finally:
        if conn:
            conn.close() # Garante que a conexão seja fechada mesmo em caso de erro

@app.route('/api/receber_dados', methods=['POST'])
def receber_dados():
    dados = request.get_json()
    
    temperatura = dados.get('temperatura')
    umidade = dados.get('umidade')
    gas_ppm = dados.get('gas')
    
    conn = None # Inicializa conn para garantir que esteja definido
    try:
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO sensores (temperatura, umidade, gas_ppm)
            VALUES (%s, %s, %s)
        """, (temperatura, umidade, gas_ppm))
        conn.commit()
        cur.close()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        print(f"Erro ao receber dados: {e}") # Imprime o erro para depuração
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn:
            conn.close() # Garante que a conexão seja fechada mesmo em caso de erro

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)