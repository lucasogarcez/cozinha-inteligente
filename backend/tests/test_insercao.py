import psycopg2
import random
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis do arquivo .env

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
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
