import datetime 

import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_fiis():
    """
    Realiza o web scraping dos dados de FIIs do Fundamentus.

    Returns:
        pandas.DataFrame: DataFrame com os dados brutos dos FIIs.
    """
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
    return df

if __name__ == '__main__':
    df_fiis = scrape_fiis()
    print(df_fiis.head())
