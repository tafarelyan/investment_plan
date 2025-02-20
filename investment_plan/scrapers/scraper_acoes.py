# Análise de ações feita com base no vídeo https://www.youtube.com/watch?v=oc0Bd5DKWdA

import datetime

import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_acoes():
    """
    Realiza o web scraping dos dados de ações do Fundamentus.

    Returns:
        pandas.DataFrame: DataFrame com os dados brutos dos ações.
    """
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

    return df

if __name__ == '__main__':
    df_acoes = scrape_acoes()
    print(df_acoes.head())