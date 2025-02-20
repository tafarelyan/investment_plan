import datetime

import pandas as pd
from investment_plan.data.data_handler import converter_valores_numericos

def analyze_fiis(df_fiis):
    """
    Analisa o DataFrame de FIIs, aplicando critérios de seleção e ranking.

    Args:
        df_fiis (pandas.DataFrame): DataFrame com os dados brutos de FIIs.

    Returns:
        pandas.DataFrame: DataFrame com os FIIs classificados e filtrados.
    """
    df = df_fiis.copy() # Boa prática para não modificar o DataFrame original

    df[df.columns.difference(['Papel', 'Segmento', 'Qtd de imóveis', 'Endereço'])] = df[df.columns.difference(['Papel', 'Segmento', 'Qtd de imóveis', 'Endereço'])].apply(converter_valores_numericos)
    1

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

    return df

if __name__ == '__main__':
    from investment_plan.scrapers.scraper_fiis import scrape_fiis
    df_bruto = scrape_fiis()
    df_analisado = analyze_fiis(df_bruto)
    print(df_analisado.head())