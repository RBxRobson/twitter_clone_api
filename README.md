# Readme ainda está em criação atualmente é apenas um rascunho lembrete

## Rotas:

### Login:

URLAPP/accounts/login/

#### Campos Json:

username e password

### CRUD Users:

#### Rota default

URLAPP/accounts/users/

#### Campos Json para criação de usuário:

name, email e password

#### Acessar usuário

URLAPP/accounts/users/#USERID#/

#### Formato Json para alterações no usuário

{
name: obrigatório(vai ser alterado futuramente)
email: obrigatório(vai ser alterado futuramente)
profile: { opcionais
bio:
avatar: URL
header: URL
}
}

### CRUD Post (Tweets)

Para todas os métodos envolvendo a rota postings/, é necessário token de autenticação gerado pelo jwt no login do usuário

#### Rota default

URLAPP/postings/posts/

#### Campos Json para criação de post:

author(username) e content

#### Acessar post

URLAPP/accounts/users/#POSTID#/

#### Comentar post

URLAPP/accounts/users/#POSTID#/comment/

#### Campos Json para comentarios

Para um comentário em um post apenas o campo "content", para resposta a um comentário deve ser incluído o campo "parent_comment" com o id do comentário a ser respondido

#### Curtir um post

URLAPP/accounts/users/#POSTID#/like/
OBS: Sem campos a serem preenchidos
