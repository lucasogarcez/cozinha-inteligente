from flask import Flask, render_template, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Configurações do banco
db_config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'cozinha',
    'user': 'seu_usuario',
    'password': 'sua_senha'
}

def conectar_db():
    return psycopg2.connect(**db_config)

@app.route('/api/dados')
def get_data():
    conn = conectar_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Busca os últimos 10 registros
    cur.execute("""
        SELECT data_hora, temperatura, umidade
        FROM sensores
        ORDER BY data_hora DESC
        LIMIT 10
    """)
    registros = cur.fetchall()
    cur.close()
    conn.close()

    # Prepara os dados para o gráfico
    registros.reverse()  # do mais antigo pro mais novo
    dados = {
        "labels": [r['data_hora'].strftime('%H:%M:%S') for r in registros],
        "temperatura": [r['temperatura'] for r in registros],
        "umidade": [r['umidade'] for r in registros]
    }
    return jsonify(dados)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
