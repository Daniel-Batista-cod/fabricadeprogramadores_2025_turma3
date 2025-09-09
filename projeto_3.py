import sqlite3 

try: 
    con = sqlite3.connect("desafio.db")
    cur = con.cursor()

    cur.execute("DELETE FROM pessoa")
    #cur.execute("CREATE TABLE  pessoa(id,nome, sala)")
    cur.execute("INSERT INTO pessoa VALUES ('1', 'ana', 'recepção')")
    cur.execute("INSERT INTO pessoa VALUES ('2','bruno', 'financeiro')")
    cur.execute("INSERT INTO  pessoa VALUES('3', 'carla', 'deposito')")
    con.commit()

    cur.execute("SELECT * FROM pessoa")
    responsavel = cur.fetchone()

    if responsavel:
        print("quem esta com a chave do deposito:{responsavel[0]}")

    else:
        print("nenhum responsavel encontrado para o deposito.")

    con.commit()
except sqlite3.Error as e:
    print("erro:",e)

