import datetime

import pandas as pd
from investment_plan.data.data_handler import converter_valores_numericos


def analyze_acoes(df_acoes):
    """
    Analisa o DataFrame de FIIs, aplicando critérios de seleção e ranking.

    Args:
        df_fiis (pandas.DataFrame): DataFrame com os dados brutos de FIIs.

    Returns:
        pandas.DataFrame: DataFrame com os FIIs classificados e filtrados.
    """

    df = df_acoes.copy() # Boa prática para não modificar o DataFrame original

    df[df.columns.difference(['Papel'])] = df[df.columns.difference(['Papel'])].apply(converter_valores_numericos)

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

    return df

if __name__ == '__main__':
    from investment_plan.scrapers.scraper_acoes import scrape_acoes
    df_bruto = scrape_acoes()
    df_analisado = analyze_acoes(df_bruto)
    print(df_analisado.head())