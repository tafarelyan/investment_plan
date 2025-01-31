# Análise de ações feita com base no vídeo https://www.youtube.com/watch?v=oc0Bd5DKWdA

import datetime

import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL da página de resultados do Fundamentus
url = "https://www.fundamentus.com.br/resultado.php"

# Headers para simular um navegador real e evitar bloqueios
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Faz a requisição HTTP
resposta = requests.get(url, headers=headers)
resposta.raise_for_status()  # Lança erro se a requisição falhar

# Parse do HTML
soup = BeautifulSoup(resposta.text, "html.parser")

# Encontrar a tabela de resultados
tabela = soup.find("table")

# Extrair os dados da tabela
dados = []
for linha in tabela.find_all("tr")[1:]:  # Ignora o cabeçalho
    colunas = linha.find_all("td")
    dados.append([coluna.text.strip() for coluna in colunas])

# Criar um DataFrame do Pandas
colunas = [th.text.strip() for th in tabela.find_all("th")]
df = pd.DataFrame(dados, columns=colunas)

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

df[df.columns.difference(['Papel'])] = df[df.columns.difference(['Papel'])].apply(converter_valores_numericos)

data_atual = datetime.datetime.now().strftime("%d-%m-%Y")
df.to_csv(f"dados_historicos/acoes_{data_atual}.csv", index=False, encoding="utf-8")

colunas_removidas = [
    'PSR',
    'P/Ativo',
    'P/Cap.Giro',
    'P/EBIT',
    'P/Ativ Circ.Liq',
    'EV/EBIT',
    'EV/EBITDA',
    'Mrg Ebit',
    'Liq. Corr.', 
    'Patrim. Líq',
    'Dív.Brut/ Patrim.',
    'Cresc. Rec.5a',
]
df = df.drop(columns=colunas_removidas)

df = df[
    (df['Cotação'] >= 1) & # Excluir penny stocks
    (df['P/L'] >= 3) & (df['P/L'] <= 10) & # Preço sobre o lucro
    # (df['P/VP'] >= 0.8) & (df['P/VP'] <= 1.5) & # Preço sobre o valor patrimonial
    (df['Div.Yield'] >= 0.05) & (df['Div.Yield'] <= 1) & # Porcentagem do preço da ação que é pago em dividendos
    (df['Mrg. Líq.'] >= 0.1) & # Margem líquida
    (df['ROE'] >= 0.1) & # Retorno sobre o patrimônio líquido
    (df['Liq.2meses'] >= 1000000) # Liquidez média diária dos últimos 2 meses
]

df = df.sort_values('P/L', ascending=True)
df['Ranking P/L'] = range(1, len(df) + 1)

df = df.sort_values('P/VP', ascending=True)
df['Ranking P/VP'] = range(1, len(df) + 1)

df = df.sort_values('Div.Yield', ascending=False)
df['Ranking DY'] = range(1, len(df) + 1)

df = df.sort_values('Mrg. Líq.', ascending=False)
df['Ranking ML'] = range(1, len(df) + 1)

df = df.sort_values('ROE', ascending=False)
df['Ranking ROE'] = range(1, len(df) + 1)

df['Ranking Final'] = df[['Ranking P/L', 'Ranking P/VP', 'Ranking DY', 'Ranking ML', 'Ranking ROE']].sum(axis=1)
df = df.sort_values('Ranking Final', ascending=True)

df.to_csv(f"classificacao_acoes.csv", index=False, encoding="utf-8")