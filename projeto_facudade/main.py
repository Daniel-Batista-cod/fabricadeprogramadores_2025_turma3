from tabelas import SessionLocal, Usuario, Nota

db = SessionLocal()

def criar_novo_usuario_e_nota(novo_usuario: Usuario, nova_nota: Nota):

    db.add(novo_usuario)
    db.commit()
    print(f"Usuario '{novo_usuario.nome}' criado com ID: {novo_usuario.id}")

    db.add(nova_nota)
    db.commit


def autualizar_nota(id_nota: int):

    nota_para_editar = db.query(Nota).filter(Nota.id == id_nota).first()

    if nota_para_editar:
        print(f"conteudo original: '{nota_para_editar.conteudo}'")
        nota_para_editar= "Lista de anotações ATUALIZADA!"
        db.commit()
        print(f"conteudo novo: '{nota_para_editar.conteudo}'")
    else:
        print("Nota com ID % não encontrada." % id_nota)

def ler_dados():

    users = db.query(Usuario).all()

    if users:
        
        for nota in users.notas:
            print(f"  - conteudo: {nota.conteudo} (ID {nota.id})")
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