import psycopg2
import random
from datetime import datetime

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='cozinha',
    user='seu_usuario',
    password='sua_senha'
)
cur = conn.cursor()

for _ in range(10):
    temperatura = round(random.uniform(24, 30), 2)
    umidade = round(random.uniform(50, 70), 2)
    gas = round(random.uniform(200, 500), 2)

    cur.execute("""
        INSERT INTO sensores (temperatura, umidade, gas_ppm)
        VALUES (%s, %s, %s)
    """, (temperatura, umidade, gas))

conn.commit()
cur.close()
conn.close()
print("Dados inseridos com sucesso!")
