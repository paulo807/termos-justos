import spacy
import re

# Carrega modelo de português
nlp = spacy.load('pt_core_news_sm')

# Lista de padrões abusivos (regex simples)
PADROES_ABUSIVOS = [
    r"cancelamento unilateral",
    r"taxa oculta",
    r"alteração de preço sem consentimento",
    r"renúncia de direitos",
]

def analisar_clausula(texto):
    """
    Analisa uma cláusula e retorna True se for abusiva.
    """
    doc = nlp(texto.lower())

    # Verifica padrões por regex
    for padrao in PADROES_ABUSIVOS:
        if re.search(padrao, texto.lower()):
            return True

    # Futuro: equivalências semânticas com embeddings
    return False