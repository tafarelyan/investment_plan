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
        col = col.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)

        if "%" in col.iloc[0]:
            col = col.str.replace("%", "", regex=False).apply(lambda x: x.replace(",", ".") if isinstance(x, str) else x).astype(float) / 100
            col = round(col * 100000) / 100000
        else:
            col = pd.to_numeric(col, errors='coerce')
            col = col.fillna(0.0)
            col = round(col * 1000) / 1000

    return col