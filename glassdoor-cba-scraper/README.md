# Glassdoor CBA Scraper
Este projeto é um conjunto de ferramentas para coletar, analisar e visualizar avaliações de funcionários do Glassdoor. Ele utiliza a API da Wextractor para extrair os dados e bibliotecas de Python como Pandas, Matplotlib e WordCloud para processar e apresentar as informações.

## Funcionalidades
- **Coleta de Dados:** Extrai todas as avaliações de uma empresa específica no Glassdoor.
- **Análise Quantitativa:** Calcula médias de avaliação por categoria e localidade.
- **Visualização de Dados:** Gera gráficos de barras e nuvens de palavras para representar os dados.
- **Análise de Texto:** Identifica os termos mais comuns (prós e contras) e permite a busca por palavras-chave.
- **Geração de Relatórios:** Cria relatórios formatados em `.txt` com as avaliações.

## Como Usar
### 1. Pré-requisitos

- Python 3.x
- As dependências listadas no arquivo `requirements.txt`.

Para instalar as dependências, execute:
```bash
pip install -r requirements.txt
```

### 2. Configuração

Antes de executar o coletor, você precisa configurar seu token de autenticação da Wextractor:

1.  Abra o arquivo `coletor_glassdoor.py`.
2.  Insira seu `AUTH_TOKEN` na variável correspondente. Você pode obter um token em [wextractor.com](https://wextractor.com/account/).
3.  (Opcional) Altere o `COMPANY_ID` para a empresa que você deseja analisar.

### 3. Ordem de Execução dos Scripts

1.  **`coletor_glassdoor.py`**: Execute este script primeiro para baixar as avaliações e gerar o arquivo `glassdoor_reviews.csv`.
2.  **`analisador.py`**: Após a coleta, execute este script para gerar os gráficos e as nuvens de palavras principais.
3.  **Outros Scripts (Opcional)**:
    - `explorador_texto.py`: Para uma análise interativa de termos e palavras-chave.
    - `extrator_pros_contras.py`: Para extrair os prós e contras em arquivos de texto separados.
    - `gerador_nuvem_termos.py`: Para gerar nuvens de palavras baseadas em bigramas e trigramas.
    - `gerador_relatorio_completo.py`: Para criar um relatório consolidado de todas as avaliações.

## Descrição dos Scripts

- **`coletor_glassdoor.py`**: Conecta-se à API da Wextractor, baixa todas as avaliações da empresa configurada e as salva no arquivo `glassdoor_reviews.csv`.
- **`analisador.py`**: Lê o arquivo `.csv`, calcula as médias de avaliação e gera os seguintes arquivos de imagem:
    - `grafico_medias_gerais.png`
    - `grafico_media_por_localidade.png`
    - `nuvem_pontos_positivos.png`
    - `nuvem_pontos_negativos.png`
- **`explorador_texto.py`**: Um script interativo para explorar o conteúdo textual das avaliações. Ele exibe os termos mais comuns e permite que o usuário busque por palavras-chave específicas.
- **`extrator_pros_contras.py`**: Extrai os comentários "prós" e "contras" do `.csv` e os salva em `pros_formatado.txt` e `contras_formatado.txt`, respectivamente.
- **`gerador_nuvem_termos.py`**: Gera nuvens de palavras mais avançadas, baseadas na frequência de bigramas e trigramas (termos com 2 e 3 palavras), salvando-as como `nuvem_termos_positivos.png` e `nuvem_termos_negativos.png`.
- **`gerador_relatorio_completo.py`**: Cria um arquivo `relatorio_completo.txt` que formata cada avaliação em um "card" de fácil leitura.

## Arquivos Gerados

- `glassdoor_reviews.csv`: O arquivo de dados brutos com todas as avaliações.
- `grafico_*.png`: Gráficos de barras com as médias de avaliação.
- `nuvem_*.png`: Nuvens de palavras geradas a partir dos prós e contras.
- `relatorio_*.txt`: Relatórios de texto com as avaliações formatadas.
