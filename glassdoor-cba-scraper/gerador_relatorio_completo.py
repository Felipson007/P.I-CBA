# gerador_relatorio_completo.py
import pandas as pd
import os

# --- CONFIGURAÇÃO ---
ARQUIVO_ENTRADA_CSV = 'glassdoor_reviews.csv'
ARQUIVO_SAIDA_RELATORIO = 'relatorio_completo.txt'
SEPARADOR = "*" * 50
# --------------------

print("Iniciando a geração do relatório completo...")

if not os.path.exists(ARQUIVO_ENTRADA_CSV):
    print(f"❌ ERRO: Arquivo '{ARQUIVO_ENTRADA_CSV}' não encontrado!")
else:
    # Carrega o arquivo CSV
    df = pd.read_csv(ARQUIVO_ENTRADA_CSV)
    
    # Abre o arquivo de saída para escrita
    with open(ARQUIVO_SAIDA_RELATORIO, 'w', encoding='utf-8') as f:
        # Itera por cada linha do DataFrame
        for index, row in df.iterrows():
            
            # Pega as informações de cada coluna da linha atual
            # .get('coluna', 'N/A') é uma forma segura de pegar o dado,
            # que retorna 'N/A' se a coluna ou o valor não existir.
            rating = row.get('rating', 'N/A')
            reviewer = row.get('reviewer', 'Cargo não informado')
            pros = row.get('pros', 'Nenhum pró informado.')
            cons = row.get('cons', 'Nenhum contra informado.')
            
            # Monta o "card" de informações formatado
            f.write(f"AVALIAÇÃO GERAL: {rating} de 5 estrelas\n")
            f.write(f"CARGO: {reviewer}\n")
            f.write("-" * 20 + "\n") # uma linha menor para separar o conteúdo
            f.write(f"✅ PRÓS:\n{pros}\n\n")
            f.write(f"❌ CONTRAS:\n{cons}\n")
            
            # Escreve o separador principal e duas linhas em branco
            f.write(SEPARADOR + "\n\n")
            
    print(f"✅ Sucesso! O relatório consolidado foi salvo em: {ARQUIVO_SAIDA_RELATORIO}")

print("\nGeração do relatório concluída.")