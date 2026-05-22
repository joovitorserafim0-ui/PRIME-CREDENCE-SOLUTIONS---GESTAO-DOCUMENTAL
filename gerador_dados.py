import pandas as pd
import random
from datetime import datetime, timedelta

def gerar_dados_complexos(n=500):
    clientes = ["AutoClick Veículos", "FastCred Financiamentos", "TopCar Revenda", "Global Motors", "Elite Autos", "Vip Veículos"]
    status_op = ["Concluído", "Parado", "Em Andamento"]
    
    dados = []
    for i in range(1, n + 1):
        data_inicio = datetime.now() - timedelta(days=random.randint(1, 45))
        valor = random.uniform(20000, 200000)
        status = random.choices(status_op, weights=[0.6, 0.2, 0.2])[0]
        
        # Lógica de risco
        dias_parado = (datetime.now() - data_inicio).days if status == "Parado" else 0
        risco = "ALTO" if (valor > 150000 or (status == "Parado" and dias_parado > 15)) else "BAIXO"
        
        dados.append([i, random.choice(clientes), valor, status, data_inicio.strftime('%Y-%m-%d'), dias_parado, risco])
    
    return pd.DataFrame(dados, columns=['id', 'loja', 'valor', 'status', 'data_inicio', 'dias_parado', 'margem_risco'])

# Gera e sobrescreve o arquivo antigo
df = gerar_dados_complexos(500)
df.to_csv('base_diaria_financeira.csv', index=False)
print("Arquivo CSV atualizado com sucesso!")