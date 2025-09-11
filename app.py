from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

BANCO_DE_DADOS = "bloco_de_notas.db"

def get_db():
    db = sqlite3.connect(BANCO_DE_DADOS)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit
    

def new_note(nota):
    con = sqlite3.connect(BANCO_DE_DADOS)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO anotacoes (texto, data_hora)
        VALUES(%, datatime('now))
""" % nota)
    con.commit()
    con.close()
    con.close()


@app.route('/iniciar')
def iniciar ():
    init_db()
    return 'Banco de daddos iniciado...'
 
@app.route('/home', methods = ["GET"])
def home ():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM anotacoes')
        dados = cursor.fetchall()
        return jsonify([dict(row) for row in dados])
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/')
def index():
    return '''<h1> Bloco de notas </h1>
            <h2> Rotas:</h2>
            <ul>
                <li>
                    <a href="/iniciar">/iniciar</a>
                </li>
                <li>
                    <a href="/home">/home</a>
                </li>
            </ul>
    '''