import _sqlite3
from bs4 import BeautifulSoup
from database import inserir_termo_abusivo, listar_termos_abusivos

# HTML fictício simulando uma página com cláusulas abusivas
html = """
<ul>
    <li>Cancelamento unilateral sem aviso prévio</li>
    <li>Cobrança de taxa oculta</li>
    <li>Alteração de preço sem consentimento</li>
</ul>
"""

# Analisa o HTML com BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Extrai todas as cláusulas dentro de <li>
clausulas = [li.text.strip() for li in soup.find_all('li')]

# Insere cada cláusula na base de dados
for c in clausulas:
    inserir_termo_abusivo(c, 'grave', 'pagina_ficticia')

# Lista os termos para confirmar
for termo in listar_termos_abusivos():
    print(termo)