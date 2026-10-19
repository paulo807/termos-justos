from idlelib.rpc import response_queue

import requests
from bs4 import BeautifulSoup
from database import inserir_termo_abusivo, listar_termos_abusivos

def scraping_real(url):
    # 1. Faz requisição HTTP
    response = requests.get(url)
    response.raise_for_status() # erro se não carregar

    # 2. Analisa HTML
    soup = BeautifulSoup(response.text, 'lxml')

    # 3. Extrai cláusulas (exemplo: dentro de <li>)
    clausulas = [li.text.strip() for li in soup.find_all('li')]

    # 4. Insere na base de dados
    for c in clausulas:
        inserir_termo_abusivo(c, 'grave', url)

    print(f'foram inseridas {len(clausulas)} clausulas da fonte: {url}')

    # 5. Lista para confirmar
    for termo in listar_termos_abusivos():
        print(termo)

# Teste com site da União Europeia
scraping_real('https://www.viecelliadvogados.com.br/artigos/juros-abusivos-emprestimo-pessoal-2026.html')