import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# --- CONFIGURAÇÃO ---
NOME_ARQUIVO_CSV = 'glassdoor_reviews.csv'
# --------------------


def analisar_reviews(nome_arquivo_csv):
    """
    Lê um arquivo CSV de reviews do Glassdoor e gera um relatório de análise
    com gráficos e nuvens de palavras.
    """
    print(f"--- Iniciando a análise do arquivo: {nome_arquivo_csv} ---")

    # Verifica se o arquivo existe antes de continuar
    if not os.path.exists(nome_arquivo_csv):
        print(f"❌ ERRO CRÍTICO: Arquivo '{nome_arquivo_csv}' não encontrado!")
        print("Por favor, verifique se o script 'analisador.py' está na MESMA PASTA que o seu arquivo CSV.")
        return # Para a execução
        
    # 1. Carregar os dados do arquivo CSV
    df = pd.read_csv(nome_arquivo_csv)
    print("✅ Arquivo CSV carregado com sucesso.")

    # 2. Limpeza e Preparação dos Dados
    colunas_rating = [
        'rating', 'culture_and_values_rating', 'diversity_and_inclusion_rating',
        'work_life_balance_rating', 'senior_management_rating',
        'compensation_and_benefits_rating', 'career_opportunities_rating'
    ]
    # Converte colunas de avaliação para número, tratando erros
    for col in colunas_rating:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove linhas onde a avaliação principal ('rating') não existe
    df.dropna(subset=['rating'], inplace=True)
    
    # Limpa a coluna de localização para agrupar melhor os dados (ex: "São Paulo, " vira "São Paulo")
    if 'location' in df.columns:
        df['location'] = df['location'].str.strip().str.replace(',','')
    
    print("✅ Dados limpos e preparados para análise.")

    # 3. Análise Quantitativa (Resultados no Console)
    print("\n" + "="*40)
    print("📊 ANÁLISE QUANTITATIVA")
    print("="*40)
    
    media_ratings = df[colunas_rating].mean().sort_values(ascending=False)
    print("\n--- Média das Avaliações (de 0 a 5) ---")
    print(media_ratings.round(2))
    
    print("\n--- Distribuição da Nota Geral ('rating') ---")
    print(df['rating'].value_counts().sort_index())

    # 4. Geração de Gráficos e Nuvens de Palavras
    print("\n" + "="*40)
    print("🎨 GERANDO VISUALIZAÇÕES (ARQUIVOS .PNG)")
    print("="*40)

    # Gráfico 1: Médias Gerais
    plt.figure(figsize=(12, 8))
    sns.barplot(x=media_ratings.values, y=media_ratings.index, orient='h', palette='viridis')
    plt.title('Média Geral por Categoria de Avaliação', fontsize=16, weight='bold')
    plt.xlabel('Média da Nota (0-5)', fontsize=12)
    plt.ylabel('')
    plt.xlim(0, 5) # Garante que a escala do eixo X vai de 0 a 5
    plt.tight_layout()
    plt.savefig('grafico_medias_gerais.png')
    print("✅ Gráfico 'grafico_medias_gerais.png' foi salvo!")

    # Gráfico 2: Média por Localidade (se a coluna existir)
    if 'location' in df.columns and not df['location'].isnull().all():
        media_por_local = df.groupby('location')['rating'].mean().nlargest(10).sort_values(ascending=True)
        plt.figure(figsize=(12, 8))
        sns.barplot(x=media_por_local.values, y=media_por_local.index, orient='h', palette='plasma')
        plt.title('Top 10 Localidades com Melhor Média de Avaliação', fontsize=16, weight='bold')
        plt.xlabel('Média da Nota', fontsize=12)
        plt.ylabel('Localidade', fontsize=12)
        plt.tight_layout()
        plt.savefig('grafico_media_por_localidade.png')
        print("✅ Gráfico 'grafico_media_por_localidade.png' foi salvo!")

    # Nuvem de Palavras 1: Pontos Positivos
    # Junta todos os textos da coluna 'pros', ignorando os que estiverem vazios
    texto_pros = " ".join(review for review in df.pros.dropna())
    if texto_pros:
        wordcloud_pros = WordCloud(width=1200, height=600, background_color='white', collocations=False).generate(texto_pros)
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud_pros, interpolation='bilinear')
        plt.axis("off")
        plt.title('Principais Pontos Positivos Mencionados', fontsize=20, weight='bold')
        plt.tight_layout()
        plt.savefig('nuvem_pontos_positivos.png')
        print("✅ Nuvem de palavras 'nuvem_pontos_positivos.png' foi salva!")

    # Nuvem de Palavras 2: Pontos Negativos
    texto_cons = " ".join(review for review in df.cons.dropna())
    if texto_cons:
        wordcloud_cons = WordCloud(width=1200, height=600, background_color='black', colormap='Reds', collocations=False).generate(texto_cons)
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud_cons, interpolation='bilinear')
        plt.axis("off")
        plt.title('Principais Pontos Negativos Mencionados', fontsize=20, weight='bold')
        plt.tight_layout()
        plt.savefig('nuvem_pontos_negativos.png')
        print("✅ Nuvem de palavras 'nuvem_pontos_negativos.png' foi salva!")

    print("\n--- Análise Concluída! Verifique os arquivos .png na pasta. ---")


# --- PONTO DE PARTIDA DO SCRIPT ---
if __name__ == '__main__':
    analisar_reviews(NOME_ARQUIVO_CSV)