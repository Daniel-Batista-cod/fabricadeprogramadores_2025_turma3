from flask import Flask, request, jsonify, render_template, json, redirect, url_for
from main import (
    autualizar_nota,
    login_de_usuario,
    matricular_aluno,
    criar_novo_usuario_e_nota,
    deletar_usuario,
    ler_dados,
    Usuario,
    Nota
)

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        try:
            usuario_e_nota = request.get_json()

            user = Usuario(
                nome=usuario_e_nota["usuario"],
                email=usuario_e_nota["email"],
                senha_hash=usuario_e_nota["senha"]
            )
            note = Nota(
                titulo=usuario_e_nota["titulo"],
                conteudo=usuario_e_nota["nota"]
            )

            app.logger.info("Usuário está criando nota e usuário associado.")
            criar_novo_usuario_e_nota(user, note)

            return jsonify({"success": True, "msg": "Usuário e nota criados com sucesso!"}), 201

        except Exception as e:
            app.logger.error("Erro ao criar usuário e nota: %s", str(e))
            return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/users", methods=["GET"])
def api_users():
    try:
        data = ler_dados()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/home", methods=["GET"])
def home():
    try:
        return render_template("home.html")
    except:
        return render_template("mandioca.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            usuario = request.get_json()

            user = Usuario(email=usuario["email"], senha_hash=usuario["senha_hash"])
            usr = login_de_usuario(user)

            app.logger.info("Usuário de email: %s logado com sucesso!" % usuario["email"])

            return jsonify({"success": True, "msg": f"Usuário {usuario['email']} logado com sucesso!"}), 200

        except Exception as e:
            app.logger.error("Erro no login: %s", str(e))
            return jsonify({"success": False, "error": str(e)}), 401

    else:
        try:
            return render_template("login.html")
        except:
            return render_template("mandioca.html")

@app.route("/remover/usuarios/<id>", methods=['GET', 'DELETE'])
def remover_usuarios(id):
    if request.method == "DELETE":
        try:
            deletar_usuario(id_usuario=id)
            app.logger.info("Usuário do ID: %s foi removido com sucesso!" % id)
            return jsonify({"success": True, "msg": f"Usuário {id} removido com sucesso!"}), 200

        except Exception as e:
            app.logger.error("Erro na remoção de usuário: %s", str(e))
            return jsonify({"success": False, "error": str(e)}), 500
    else:
        return render_template('remover.html')


@app.route("/matricula/<id_usuario>/<id_curso>", methods=['GET', 'POST'])
def matricula(id_usuario, id_curso):
    if request.method == 'POST':
        try:
            matricular_aluno(id_aluno=id_usuario, id_curso=id_curso)
            app.logger.info(f"Usuário {id_usuario} matriculado no curso {id_curso}")
            return jsonify({"success": True, "msg": "Matrícula realizada com sucesso!"}), 200

        except Exception as e:
            app.logger.error("Erro na matrícula do usuário: %s", str(e))
            return jsonify({"success": False, "error": str(e)}), 500

    return render_template("matricula.html", id_usuario=id_usuario, id_curso=id_curso)


if __name__ == "__main__":
    app.run(debug=True)