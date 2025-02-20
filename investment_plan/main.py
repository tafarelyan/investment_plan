import datetime
from investment_plan.scrapers.scraper_acoes import scrape_acoes
from investment_plan.scrapers.scraper_fiis import scrape_fiis
from investment_plan.analyzers.analyzer_acoes import analyze_acoes
from investment_plan.analyzers.analyzer_fiis import analyze_fiis

def processar_fiis():
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

def processar_acoes():
    print("Iniciando scraping de Ações...") # Log simples (melhor usar logging mais estruturado)
    df_acoes_bruto = scrape_acoes()
    print("Scraping de Ações concluído.")

    data_atual = datetime.datetime.now().strftime("%d-%m-%Y")
    output_path = f"data/raw_data/acoes_{data_atual}.csv" # Use a pasta output
    df_acoes_bruto.to_csv(output_path, index=False, encoding="utf-8")
    print(f"CSV de Ações raw salvo em: {output_path}")

    print("Iniciando análise de Ações...")
    df_acoes_classificados = analyze_acoes(df_acoes_bruto)
    print("Análise de Ações concluída.")

    output_path = f"data/output/acoes_classificados_{data_atual}.csv" # Use a pasta output
    df_acoes_classificados.to_csv(output_path, index=False, encoding="utf-8")
    print(f"CSV de Ações classificados salvo em: {output_path}")


def main():
    """Função principal para orquestrar o processamento de FIIs e Ações."""

    processar_fiis()
    processar_acoes()


if __name__ == "__main__":
    main()