# extrator_formatado.py
import pandas as pd
import os

# --- CONFIGURAÇÃO ---
ARQUIVO_ENTRADA_CSV = 'glassdoor_reviews.csv'
ARQUIVO_SAIDA_PROS = 'pros_formatado.txt'
ARQUIVO_SAIDA_CONTRAS = 'contras_formatado.txt'
SEPARADOR = "=" * 50 
# --------------------

print("Iniciando a extração formatada dos prós e contras...")

if not os.path.exists(ARQUIVO_ENTRADA_CSV):
    print(f"❌ ERRO: Arquivo '{ARQUIVO_ENTRADA_CSV}' não encontrado!")
else:
    df = pd.read_csv(ARQUIVO_ENTRADA_CSV)
    
    # --- Processando os PRÓS ---
    pros = df['pros'].dropna()
    with open(ARQUIVO_SAIDA_PROS, 'w', encoding='utf-8') as f:
        for pro in pros:
            # Escreve o comentário
            f.write(str(pro) + '\n')
            # Escreve o separador e duas linhas em branco para espaçamento
            f.write(SEPARADOR + '\n\n')
            
    print(f"✅ Sucesso! {len(pros)} comentários 'Prós' foram salvos em: {ARQUIVO_SAIDA_PROS}")

    # --- Processando os CONTRAS ---
    contras = df['cons'].dropna()
    with open(ARQUIVO_SAIDA_CONTRAS, 'w', encoding='utf-8') as f:
        for contra in contras:
            # Escreve o comentário
            f.write(str(contra) + '\n')
            # Escreve o separador e duas linhas em branco para espaçamento
            f.write(SEPARADOR + '\n\n')
            
    print(f"✅ Sucesso! {len(contras)} comentários 'Contras' foram salvos em: {ARQUIVO_SAIDA_CONTRAS}")

print("\nExtração concluída.")