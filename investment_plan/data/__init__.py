import pandas as pd


def converter_valores_numericos(col):
    """
    Converte valores de uma coluna de DataFrame para numérico, tratando formatos diversos.

    Args:
        col (pandas.Series): Coluna do DataFrame.

    Returns:
        pandas.Series: Coluna com valores numéricos convertidos.
    """
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