import requests

resp = requests.get("http://localhost:5000/api/dados")
if resp.ok:
    print("✅ Dados recebidos:")
    print(resp.json())
else:
    print("❌ Erro:", resp.status_code)
