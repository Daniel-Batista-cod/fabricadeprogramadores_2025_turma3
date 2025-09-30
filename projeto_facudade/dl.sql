UPDATE usuario SET nome = 'Bernadino' WHERE id = 1;

UPDATE usuario SET (nome,email,senha,senha_hash) = ('Lazaro','lazaro@gmail.com', '1234')
    WHERE id = 1;
SELECT (rua) FROM enderecos;
--comentario do postgreSQL

DELETE FROM enderecos;
DELETE FROM usuarios;
DELETE FROM notas;

--curval pega o valor atual 
SELECT curval('endereco_id_seq');

--nextval pega o proximo
SELECT nextval('endereco_id_seq');