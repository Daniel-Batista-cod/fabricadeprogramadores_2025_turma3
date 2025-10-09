from tabelas import SessionLocal, Usuario, Nota,Cursos, joinedload

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
        
        usuarios = db.query(Usuario).options(joinedload(Usuario.notas)).filter(
                 Usuario.id== usuario_deletado.id).all()
        for u in usuarios:
            for n in u.notas:
                nota_deletada = db.query(Nota).filter(Nota.id==n.id).first()
                db.delete(nota_deletada)
                db.commit()
                db.flush()        

        db.delete(usuario_deletado)
        db.commit()

        print(f"Usuario: '{usuario_deletado.nome}' removido com sucesso!")       
    else:
        print("Nota com ID % não encontrada." % id_usuario)

def login_de_usuario(usr:Usuario):
    usuario_logado = db.query(Usuario).filter(
        Usuario.email ==usr.email and Usuario.senha_hash == usr.senha_hash).first()
    

    resultado = []
    if usuario_logado:
        resultado.append({
            "id": usuario_logado.id,
            "usuario": usuario_logado.nome,
            "email": usuario_logado.email,
            "criado_em": usuario_logado.criado_em
        })
        return resultado
    
    else:
        print("Usuario não encontrado")


def matricular_aluno(id_aluno: int, id_curso: int):
    curso = db.query(Cursos).filter(Cursos.id == id_curso).first()
    aluno = db.query(Usuario).filter(Usuario.id == id_aluno).first()

    if (curso and aluno):
        aluno.usuario_cursos.append(curso)
        db.commit()

        return print(f'aluno: {aluno.nome} matriculado em {curso.nome} com sucesso!')
    
    else:
        print('Erro ao realizar a matricula.')