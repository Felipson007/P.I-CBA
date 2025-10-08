import requests
import csv
import math
import time

# --- CONFIGURAÇÃO ---
# Obter API TOKEN em https://wextractor.com/account/
AUTH_TOKEN = '' 
COMPANY_ID = '2482906'
LANGUAGE = 'pt'
# --------------------

# --- CONFIGURAÇÃO DE TENTATIVAS ---
MAX_RETRIES = 3  # Número máximo de tentativas por página
RETRY_DELAY = 5  # Segundos de espera entre as tentativas
# ----------------------------------

BASE_URL = 'https://wextractor.com/api/v1/reviews/glassdoor'
REVIEWS_PER_PAGE = 10
all_reviews = []

print("🚀 Iniciando a coleta de reviews...")

try:
    # 1. Faz a primeira requisição
    params_primeira_pagina = { 'id': COMPANY_ID, 'language': LANGUAGE, 'auth_token': AUTH_TOKEN, 'offset': 0 }
    response = requests.get(BASE_URL, params=params_primeira_pagina)
    response.raise_for_status()
    data = response.json()
    all_reviews.extend(data['reviews'])
    
    total_reviews = data['totals']['review_count']
    total_pages = math.ceil(total_reviews / REVIEWS_PER_PAGE)
    
    print(f"✅ Total de reviews encontrados: {total_reviews}. Coletando {total_pages} páginas.")

    # 2. Loop para as páginas restantes
    for page_num in range(1, total_pages):
        offset = page_num * REVIEWS_PER_PAGE
        
        print(f"    - Coletando página {page_num + 1} de {total_pages} (offset={offset})...")
        
        params = { 'id': COMPANY_ID, 'language': LANGUAGE, 'auth_token': AUTH_TOKEN, 'offset': offset }
        
        # --- LÓGICA DE TENTATIVAS AUTOMÁTICAS ---
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(BASE_URL, params=params)
                response.raise_for_status() # Lança erro para status 4xx ou 5xx
                page_data = response.json()
                
                if 'reviews' in page_data and page_data['reviews']:
                    all_reviews.extend(page_data['reviews'])
                else:
                    print("    - Página vazia encontrada, finalizando a coleta.")
                    break # Sai do loop de páginas
                
                # Se deu tudo certo, sai do loop de tentativas e vai para a próxima página
                break 
            
            except requests.exceptions.HTTPError as e:
                # Se o erro for 5xx (erro de servidor), tenta de novo
                if 500 <= e.response.status_code < 600:
                    print(f"        -> Erro {e.response.status_code} no servidor. Tentativa {attempt + 1} de {MAX_RETRIES}. Tentando novamente em {RETRY_DELAY}s...")
                    time.sleep(RETRY_DELAY)
                else:
                    # Se for outro erro (como 401, 403), falha imediatamente
                    raise e
        else: # Este else pertence ao "for attempt", só executa se o loop terminar sem 'break'
            print(f"❌ Falha ao coletar a página {page_num + 1} após {MAX_RETRIES} tentativas. Abortando.")
            # Lança uma exceção para parar o script
            raise requests.exceptions.RequestException(f"Não foi possível coletar a página {page_num + 1}")
        # ----------------------------------------
            
        # Pausa entre as requisições bem-sucedidas
        time.sleep(2) 

    # 3. Salva os dados em CSV
    if not all_reviews:
        print("Nenhuma review foi coletada.")
    else:
        output_file = 'glassdoor_reviews.csv'
        headers = all_reviews[0].keys()
        
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(all_reviews)
            
        print(f"\n🎉 Sucesso! {len(all_reviews)} reviews foram salvas no arquivo: {output_file}")

except requests.exceptions.HTTPError as e:
    print(f"\n❌ Erro Crítico de HTTP: {e.response.status_code} - {e.response.text}")
    print("Verifique seu 'auth_token' e seus créditos na Wextractor.")
except Exception as e:
    print(f"\n❌ Ocorreu um erro inesperado: {e}")