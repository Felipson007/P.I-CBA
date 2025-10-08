import pandas as pd
import re
from collections import Counter
import nltk
from nltk.util import ngrams
from nltk.corpus import stopwords

# --- CONFIGURAÇÃO ---
NOME_ARQUIVO_CSV = 'glassdoor_reviews.csv'
# --------------------


def limpar_texto(texto):
    """Converte para minúsculas e remove pontuação."""
    texto = str(texto).lower()
    texto = re.sub(r'[^\w\s]', '', texto) # Remove pontuação
    return texto

def analisar_termos_comuns(df, coluna, n_termos=15):
    """
    Encontra e exibe os termos (combinações de 2 ou 3 palavras) mais comuns em uma coluna.
    """
    print(f"\n--- 🏆 Top {n_termos} Termos Mais Comuns em '{coluna}' ---")
    
    # Lista de palavras a serem ignoradas (artigos, preposições, etc.)
    palavras_ignoradas = stopwords.words('portuguese')
    
    # Junta todos os textos da coluna em um só, limpando-os
    texto_completo = " ".join(limpar_texto(txt) for txt in df[coluna].dropna())
    
    # Separa o texto em palavras (tokens)
    tokens = texto_completo.split()
    
    # Remove as palavras ignoradas
    tokens_filtrados = [palavra for palavra in tokens if palavra not in palavras_ignoradas]
    
    # Gera combinações de 2 palavras (bigramas) e 3 palavras (trigramas)
    bigramas = ngrams(tokens_filtrados, 2)
    trigramas = ngrams(tokens_filtrados, 3)
    
    # Junta as palavras de cada combinação (ex: ('plano', 'carreira') -> 'plano carreira')
    termos_completos = [" ".join(gram) for gram in bigramas] + [" ".join(gram) for gram in trigramas]
    
    # Conta a frequência de cada termo e exibe os mais comuns
    contagem = Counter(termos_completos)
    for termo, freq in contagem.most_common(n_termos):
        print(f'"{termo}" - {freq} vezes')


def buscar_palavra_chave(df):
    """
    Inicia um loop interativo para buscar palavras-chave nos prós e contras.
    """
    print("\n" + "="*50)
    print("🔍 MODO DE BUSCA INTERATIVA")
    print("="*50)
    print("Digite uma palavra-chave para buscar nos comentários.")
    print("Exemplos: salario, ambiente, gestao, oportunidade, crescimento")
    print("Digite 'sair' para encerrar.")

    while True:
        keyword = input("\nDigite a palavra-chave de busca: ").lower()

        if keyword == 'sair':
            print("Encerrando o explorador. Até mais!")
            break
        
        # Filtra o DataFrame para encontrar a palavra-chave nos prós e contras
        # 'case=False' ignora se é maiúscula ou minúscula
        # 'na=False' ignora células vazias
        resultados_pros = df[df['pros'].str.contains(keyword, case=False, na=False)]
        resultados_cons = df[df['cons'].str.contains(keyword, case=False, na=False)]

        print(f"\n--- ✅ Resultados para '{keyword}' em 'PROS' ({len(resultados_pros)}) ---")
        if not resultados_pros.empty:
            for pro in resultados_pros['pros']:
                print(f"- {pro}")
        else:
            print("Nenhum 'pró' encontrado com esta palavra.")
            
        print(f"\n--- ❌ Resultados para '{keyword}' em 'CONTRAS' ({len(resultados_cons)}) ---")
        if not resultados_cons.empty:
            for con in resultados_cons['cons']:
                print(f"- {con}")
        else:
            print("Nenhum 'contra' encontrado com esta palavra.")

# --- PONTO DE PARTIDA DO SCRIPT ---
if __name__ == '__main__':
    try:
        dataframe = pd.read_csv(NOME_ARQUIVO_CSV)
        
        # 1. Mostra o resumo inicial dos termos mais comuns
        analisar_termos_comuns(dataframe, 'pros')
        analisar_termos_comuns(dataframe, 'cons')
        
        # 2. Inicia o modo de busca interativa
        buscar_palavra_chave(dataframe)

    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo '{NOME_ARQUIVO_CSV}' não encontrado. Verifique se ele está na mesma pasta.")