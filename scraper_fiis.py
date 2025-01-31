import datetime 

import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL da página dos FIIs
url = "https://www.fundamentus.com.br/fii_resultado.php"

# Fazendo a requisição HTTP
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
response.encoding = "ISO-8859-1"

# Parseando o HTML com BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Encontrando a tabela dos FIIs
table = soup.find("table", attrs={'id': 'tabelaResultado'})


# Extraindo os dados da tabela
data = []
for row in table.find_all("tr")[1:]:  # Ignora o cabeçalho
    cols = [col.text.strip() for col in row.find_all("td")]
    data.append(cols)

# Pegando os nomes das colunas da tabela
columns = [col.text.strip() for col in table.find_all("tr")[0].find_all("th")]

# Criando um DataFrame com os dados
df = pd.DataFrame(data, columns=columns)

def converter_valores_numericos(col):
    if col.dtype == object:
        # Remover ponto de milhar e substituir vírgula por ponto
        col = col.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)

        # Se for porcentagem, remove "%" e divide por 100
        if "%" in col.iloc[0]:
            col = col.str.replace("%", "", regex=False).apply(lambda x: x.replace(",", ".") if isinstance(x, str) else x).astype(float) / 100
            col = round(col * 100000) / 100000 # Evita ponto flutuante
        else:
            # Convertendo para float com tratamento de erros
            col = pd.to_numeric(col, errors='coerce')  # valores inválidos serão NaN

            # Tratar o caso de "0,00" convertido para NaN
            col = col.fillna(0.0)  # Substitui NaN por 0.0, se necessário
            col = round(col * 1000) / 1000 # Evita ponto flutuante
    
    return col

df[df.columns.difference(['Papel', 'Segmento', 'Qtd de imóveis', 'Endereço'])] = df[df.columns.difference(['Papel', 'Segmento', 'Qtd de imóveis', 'Endereço'])].apply(converter_valores_numericos)
1

data_atual = datetime.datetime.now().strftime("%d-%m-%Y")
df.to_csv(f"dados_historicos/fiis_{data_atual}.csv", index=False, encoding="utf-8")

colunas_removidas = [
    'Valor de Mercado',
    'Preço do m2',
    'Aluguel por m2',
    'Cap Rate',
]
df = df.drop(columns=colunas_removidas)

df = df[
    (df['Dividend Yield'] > 0.05) &
    (df['Liquidez'] > 500000) &
    (df['P/VP'] >= 0.8) & (df['P/VP'] <= 1.2) & # Preço sobre o valor patrimonial
    (df['Vacância Média'] <= 0.10)
]

df = df.sort_values('Dividend Yield', ascending=False)
df['Ranking DY'] = range(1, len(df) + 1)

df = df.sort_values('P/VP', ascending=True)
df['Ranking P/VP'] = range(1, len(df) + 1)

df['Ranking Final'] = df[['Ranking DY', 'Ranking P/VP']].sum(axis=1)
df = df.sort_values('Ranking Final', ascending=True)

df.to_csv(f"classificacao_fiis.csv", index=False, encoding="utf-8")