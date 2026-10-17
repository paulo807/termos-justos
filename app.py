from flask import Flask, render_template, request, Response
from werkzeug.utils import secure_filename
import PyPDF2
from config import *
from utils import *
from database import *


app = Flask(__name__)

criar_tabela()

ultimo_texto_destacado = ""
ultimo_abusivas = []
ultimo_resumo = ""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analisar', methods=['POST'])
def analisar():
    texto = ''

    # 1. Se o utilizador colou texto
    if 'termos' in request.form and request.form['termos'].strip():
        texto = request.form['termos']

    # 2. Se o utilizador enviou ficheiro
    elif 'ficheiro' in request.files:
        ficheiro = request.files['ficheiro']
        if ficheiro and ficheiro.filename:
            filename = secure_filename(ficheiro.filename)
            # Se for TXT
            if filename.lower().endswith(".txt"):
                texto = ficheiro.read().decode("utf-8")
            # Se for PDF (vamos implementar depois)
            elif filename.lower().endswith(".pdf"):
                reader = PyPDF2.PdfReader(ficheiro.stream)
                texto = ""
                for page in reader.pages:
                    texto += page.extract_text() + '\n'

            elif filename.lower().endswith(".docx"):
                doc = Document(ficheiro.stream)
                texto = ""
                for para in doc.paragraphs:
                    texto += para.text + "\n"

        # ⚡ Fallback: se não houver texto nem ficheiro
        if not texto.strip():
            idioma = "unknown"
            abusivas = []
            resumo = ""
            return render_template("resultado.html",
                                   idioma=idioma,
                                   texto_destacado="",
                                   abusivas=abusivas,
                                   resumo=resumo,
                                   graves=0,
                                   moderadas=0)

    idioma = detectar_idioma(texto)
    gravidade = {"pt": gravidade_pt, "en": gravidade_en, "es": gravidade_es}.get(idioma, gravidade_pt)
    equivalencias = {"pt": equivalencias_pt, "en": equivalencias_en, "es": equivalencias_es}.get(idioma, {})

    texto_destacado, abusivas = destacar_texto(texto, gravidade, equivalencias)

    graves = sum(1 for a in abusivas if a['nivel'] == 'grave')
    moderadas = sum(1 for a in abusivas if a['nivel'] == 'moderado')
    resumo = f'Foram encontrados {len(abusivas)} cláusulas abusivas: {graves} graves e {moderadas} moderadas.'

    global ultimo_texto_destacado, ultimo_abusivas, ultimo_resumo
    ultimo_texto_destacado, ultimo_abusivas, ultimo_resumo = texto_destacado, abusivas, resumo

    salvar_analise(texto, idioma, abusivas, resumo)
    return render_template("resultado.html",
                           idioma=idioma,
                           texto_destacado=texto_destacado,
                           abusivas=abusivas,
                           resumo=resumo,
                           graves=graves,
                           moderadas=moderadas)

@app.route('/historico')
def historico():
    analises = listar_analises()
    return render_template('historico.html', analises=analises)

@app.route('/analise/<int:id>')
def ver_analise(id):
    analise = obter_analise(id)
    if analise:
        return render_template('analise.html', analise=analise)
    else:
        return 'analise nao encontrada', 404

@app.route('/download_pdf')
def download_pdf():
    response = Response(gerar_pdf(ultimo_texto_destacado, ultimo_abusivas, ultimo_resumo))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=relatorio.pdf'
    return response

@app.route('/download_docx')
def download_docx():
    response = Response(gerar_docx(ultimo_texto_destacado, ultimo_abusivas, ultimo_resumo))
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    response.headers['Content-Disposition'] = 'attachment; filename=relatorio.docx'
    return response



if __name__ == '__main__':
    app.run(debug=True)
