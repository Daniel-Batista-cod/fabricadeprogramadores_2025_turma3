from tabelas import SessionLocal, Usuario, Nota, joinedload

db = SessionLocal()

def criar_novo_usuario_e_nota(novo_usuario: Usuario, nova_nota: Nota):

    db.add(novo_usuario)
    db.commit()
    print(f"Usuario '{novo_usuario.nome}' criado com ID: {novo_usuario.id}")

    note = Nota(
        id_usuario=novo_usuario.id,
        titulo=nova_nota.conteudo
    )
    db.add(note)
    db.commit


def autualizar_nota(id_nota: int, titulo:str, conteudo: str):

    nota_para_editar = db.query(Nota).filter(Nota.id == id_nota).first()

    if nota_para_editar:
       
        nota_para_editar.titulo=titulo
        nota_para_editar.conteudo=conteudo

        db.commit()
    else:
        print("Nota com ID % não encontrada." % id_nota)

def ler_dados():

    users = db.query(Usuario).options(joinedload(Usuario.notas)).all()

    resultado = []
    for u in users:
        notas = []
        for n in u.notas:
            notas.append({
                "id": n.id,
                "titulo": n.titulo,
                "conteudo": n.conteudo,
                "criado_em": n.criado_em
            })


            resultado.append({
                "id": u.id,
                "usuario": u.nome,
                "email": u.email,
                "criado_em": u.criado_em,
                "notas": notas
            })
    return resultado

def deletar_usuario(id_usuario: int):
    usuario_deletado = db.query(Usuario).filter(Usuario.id == id_usuario).first()

    if usuario_deletado:

        db.delete(usuario_deletado)
        db.commit()

        print(f"Usuario: '{usuario_deletado.nome}' removido com sucesso!")       
    else:
        print("Nota com ID % não encontrada." % id_usuario)