# Scraper FIIs e Ações - Análise Simplificada da Bolsa

**Encontre FIIs e ações "interessantes" para investir de forma automatizada.**

Este projeto é um script Python que te ajuda a analisar rapidamente o mercado de Fundos Imobiliários (FIIs) e ações da bolsa brasileira. Ele faz o seguinte:

1.  **Coleta dados:** Busca informações atualizadas de FIIs e ações diretamente do site Fundamentus.
2.  **Analisa e classifica:** Usa critérios pré-definidos para identificar e classificar os FIIs e ações que se destacam.
3.  **Gera listas em CSV:** Cria arquivos CSV com o ranking dos FIIs e ações mais "interessantes" para você analisar.

**Como usar:**

1.  Certifique-se de ter o Python instalado.
2.  Instale as bibliotecas necessárias (você pode usar o arquivo `requirements.txt` se tiver um, ou instalar manualmente `requests`, `beautifulsoup4`, `pandas`).
3.  Execute o script principal `src/main.py` a partir da pasta raiz do projeto usando o comando: `poetry run python src/main.py` (se estiver usando Poetry) ou `python src/main.py` (se não estiver usando Poetry e tiver as dependências instaladas).
4.  Após a execução, você encontrará arquivos CSV com os resultados na pasta `data/output/`.

**O que você vai encontrar nos arquivos CSV:**

*   Listas de FIIs e ações classificadas com base em critérios de análise, prontos para você analisar com mais detalhes.

**Bibliotecas Python utilizadas:**

*   `requests`
*   `BeautifulSoup4`
*   `pandas`