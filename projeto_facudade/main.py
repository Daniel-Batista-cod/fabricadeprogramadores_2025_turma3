from tabelas import SessionLocal, Usuario, Nota

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

    users = db.query(Usuario).all()

    if users:
        
        for nota in users.notas:
            print(f"  - conteudo: {nota.titulo} (ID {nota.id})")
        return users, nota  
    else:
        print("Usuario(a) nao encontrado.")

def deletar_usuario(id_usuario: int):

    usuario_deletado = db.query(Usuario).filter(Usuario.id == id_usuario).first()

    if usuario_deletado:

        db.delete(usuario_deletado)
        db.commit()

        print(f"Usuario: '{usuario_deletado.nome}' removido com sucesso!")       
    else:
        print("Nota com ID % não encontrada." % id_usuario)