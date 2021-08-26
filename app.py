import sqlite3
from flask import Flask, request, session, g, redirect, abort, render_template, flash

# configuração
DATABASE = "blog.db"
SECRECT_KEY = 'pudim'

app = Flask(__name__)
app.config.from_object(__name__)

def conectar_bd():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def antes_requisicao():
    g.bd = conectar_bd()

@app.teardown_request
def depois_request(exc):
    g.bd.close()

@app.route('/')
@app.route('/entradas')
def exibir_entradas():
    sql = "SELECT titulo, texto FROM entradas ORDER BY id DESC"
    cur = g.bd.execute(sql)
    entradas = []
    
    entradas2 = []
    entradas2.append({'titulo': "Olá Mundo", 'texto' : "Texto desse artigo"})
    entradas2.append({'titulo': "Segundo post", 'texto' : "Texto desse segundo posto vai cair direto aqui"})

    for titulo, texto in cur.fetchall():
        entradas.append({'titulo': titulo, 'texto': texto})
    return render_template('exibir_entradas.html', entradas=entradas)

@app.route('/hello')
def pagina_inicial():
    return "Hello world, caraiu, pyrra!!"

@app.route('/inserir')
def inserir_entrada():
    if not session.get('logado'):
        abort(401)
    sql = "INSERT INTO entradas(titulo, texto) VALUES (?,?)"
    g.bd.execute(sql, request.form['campoTitulo'], request.form['campoTexto'])
    g.bd.commit()
    return redirect(url_for('exibir_entradas'))