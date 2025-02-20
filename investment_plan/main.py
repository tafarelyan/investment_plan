import datetime
from investment_plan.scrapers.scraper_fiis import scrape_fiis
from investment_plan.analyzers.analyzer_fiis import analyze_fiis


def main():
    """
    Função principal para executar o scraping, análise e geração do CSV de FIIs.
    """
    print("Iniciando scraping de FIIs...") # Log simples (melhor usar logging mais estruturado)
    df_fiis_bruto = scrape_fiis()
    print("Scraping de FIIs concluído.")

    data_atual = datetime.datetime.now().strftime("%d-%m-%Y")
    output_path = f"data/raw_data/fiis_{data_atual}.csv" # Use a pasta output
    df_fiis_bruto.to_csv(output_path, index=False, encoding="utf-8")
    print(f"CSV de FIIs raw salvo em: {output_path}")

    print("Iniciando análise de FIIs...")
    df_fiis_classificados = analyze_fiis(df_fiis_bruto)
    print("Análise de FIIs concluída.")

    output_path = f"data/output/fiis_classificados_{data_atual}.csv" # Use a pasta output
    df_fiis_classificados.to_csv(output_path, index=False, encoding="utf-8")
    print(f"CSV de FIIs classificados salvo em: {output_path}")


if __name__ == "__main__":
    main()