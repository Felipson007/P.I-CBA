# gerador_nuvem_termos.py (versão corrigida)
import pandas as pd
import re
from collections import Counter
import nltk
from nltk.util import ngrams
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# --- CONFIGURAÇÃO ---
NOME_ARQUIVO_CSV = 'glassdoor_reviews.csv'
# --------------------

def limpar_texto(texto):
    texto = str(texto).lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

def extrair_frequencia_termos(df, coluna):
    print(f"🔎 Analisando termos para a coluna '{coluna}'...")
    # CORREÇÃO AQUI: 'portuguese' em vez de 'portuguuese'
    palavras_ignoradas = stopwords.words('portuguese')
    
    texto_completo = " ".join(limpar_texto(txt) for txt in df[coluna].dropna())
    tokens = texto_completo.split()
    tokens_filtrados = [palavra for palavra in tokens if palavra not in palavras_ignoradas]
    
    bigramas = ngrams(tokens_filtrados, 2)
    trigramas = ngrams(tokens_filtrados, 3)
    
    termos_completos = [" ".join(gram) for gram in bigramas] + [" ".join(gram) for gram in trigramas]
    
    return Counter(termos_completos)

def gerar_nuvem_de_frequencias(frequencias, nome_arquivo_saida, cor_fundo='white', colormap='viridis'):
    wc = WordCloud(width=1200, height=600, 
                   background_color=cor_fundo, 
                   colormap=colormap,
                   collocations=False).generate_from_frequencies(frequencias)
    
    plt.figure(figsize=(15, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(nome_arquivo_saida)
    print(f"✅ Nuvem de palavras salva em: {nome_arquivo_saida}")


# --- PONTO DE PARTIDA DO SCRIPT ---
if __name__ == '__main__':
    if not os.path.exists(NOME_ARQUIVO_CSV):
        print(f"❌ ERRO: Arquivo '{NOME_ARQUIVO_CSV}' não encontrado.")
    else:
        dataframe = pd.read_csv(NOME_ARQUIVO_CSV)
        
        frequencias_pros = extrair_frequencia_termos(dataframe, 'pros')
        gerar_nuvem_de_frequencias(frequencias_pros, 
                                   'nuvem_termos_positivos.png', 
                                   cor_fundo='white', 
                                   colormap='viridis')

        frequencias_cons = extrair_frequencia_termos(dataframe, 'cons')
        gerar_nuvem_de_frequencias(frequencias_cons, 
                                   'nuvem_termos_negativos.png', 
                                   cor_fundo='black', 
                                   colormap='Reds')

        print("\nProcesso concluído!")