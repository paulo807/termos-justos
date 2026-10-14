import sys
import os
import pytest
# garante que a raiz do projeto está no path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

@pytest.fixture()
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Testa se a página inicial abre corretamente"""
    response = client.get('/')
    assert response.status_code ==200
    assert 'Termos Justos' in response.data.decode('utf-8')

def test_analisar_texto(client):
    """Testa envio de texto simples para análise"""
    response = client.post('/analisar', data={ 'termos': 'O contrato preve rescisao unilateral e multa excessiva'})
    assert response.status_code ==200
    assert 'recisao unilateral' in response.data.decode('utf-8') or 'multa excessiva' in response.data.decode('utf-8')

def test_analisar_sem_texto(client):
    """Testa envio vazio (fallback)"""
    response = client.post('/analisar', data={'termos': ''})
    assert response.status_code == 200
    assert "Nenhuma cláusula abusiva encontrada." in response.data.decode('utf-8')
    

