from flask import Flask, request, jsonify, render_template, json, redirect, url_for
from main import autualizar_nota, login_de_usuario
from main import criar_novo_usuario_e_nota
from main import deletar_usuario, ler_dados
from main import Usuario, Nota

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        data = request.get_data()
        usuario_e_nota = json.loads(data)

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
        return jsonify({"msg": "Usuário e nota criados com sucesso!"}), 201

    else:
        return jsonify({'error': 'Página não encontrada!'}), 404


@app.route("/api/users", methods=["GET"])
def api_users():
    try:
        data = ler_dados()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/home/<data>", methods=["GET"])
def home(data):
    return render_template("home.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_data()
        usuario = json.loads(data)

        user = Usuario(email=usuario["email"], senha_hash=usuario["senha_hash"])

        try:
            usr = login_de_usuario(user)
            app.logger.info("Usuário de email: %s logado!" % usuario["email"])
            return redirect(url_for("home", data=usr))
        except Exception as e:
            app.logger.error("Erro no servidor: %s" % str(e))
            return jsonify({"success": False, "error": str(e)}), 500

    else:
        return render_template("login.html")


@app.route("/remover/usuarios/<id>", methods=['GET', 'DELETE'])
def remover_usuarios(id):  # ✅ Recebe o parâmetro <id>
    if request.method == "DELETE":
        try:
            id_usuario = json.loads(request.data)

            deletar_usuario(id_usuario=id_usuario)

            app.logger.info("Usuário do ID: %d foi removido com sucesso!" % id_usuario)
            return redirect(url_for("index"))

        except Exception as e:
            app.logger.error("Erro na remoção de usuário: %s" % str(e))
            return jsonify({"success": False, "error": str(e)})
    else:
        return render_template('remover.html')
        

if __name__ == "__main__":
    app.run(debug=True)

