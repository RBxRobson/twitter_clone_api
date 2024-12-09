# Documentação da API (Em Desenvolvimento)

Este documento serve como referência para as rotas e funcionalidades disponíveis na API.

---

## Rotas

### Autenticação

#### Login

- URL: `URLAPP/accounts/login/`
- Método: POST
- Campos JSON:

```json
{
  "username": "string",
  "password": "string"
}
```

---

### Gerenciamento de Usuários (CRUD)

#### Lista de Usuários

- URL: `URLAPP/accounts/users/`
- Método: GET

#### Criação de Usuário

- URL: `URLAPP/accounts/users/`
- Método: POST
- Campos JSON:

```json
{
  "name": "string",
  "email": "string",
  "password": "string"
}
```

#### Detalhes do Usuário

- URL: `URLAPP/accounts/users/{USER_ID}/`
- Método: GET

#### Listagem de seguidores

- URL: `URLAPP/accounts/users/{USER_ID}/followers/`
- Método: GET

#### Listagem de seguindo

- URL: `URLAPP/accounts/users/{USER_ID}/following/`
- Método: GET

#### Seguir ou deixar de seguir

- URL: `URLAPP/accounts/users/{USER_ID}/follow/`
- URL: `URLAPP/accounts/users/{USER_ID}/unfollow/`
- Método: POST

#### Atualização de Usuário

- URL: `URLAPP/accounts/users/{USER_ID}/`
- Método: PUT/PATCH
- Formato JSON:

```json
{
  "name": "string (obrigatório)",
  "email": "string (obrigatório)",
  "profile": {
    "bio": "string (opcional)",
    "avatar": "URL (opcional)",
    "header": "URL (opcional)"
  }
}
```

---

### Gerenciamento de Postagens (CRUD)

#### Observação

Todas as operações nesta seção requerem autenticação via token JWT, gerado no login.

#### Lista de Postagens

- URL: `URLAPP/postings/posts/`
- Método: GET

#### Lista de Likes de uma postagem

- URL: `URLAPP/postings/posts/{POST_ID}/likes/`
- Método: GET

#### Lista de Comentários de uma postagem

- URL: `URLAPP/postings/posts/{POST_ID}/comments/`
- Método: GET

#### Lista de Likes de um comentário

- URL: `URLAPP/postings/posts/{POST_ID}/comments/{COMMENT_ID}/likes/`
- Método: GET

#### Lista de respostas de um comentário

- URL: `URLAPP/postings/posts/{POST_ID}/comments/{COMMENT_ID}/replies/`
- Método: GET

#### Criação de Postagem

- URL: `URLAPP/postings/posts/`
- Método: POST
- Campos JSON:

```json
{
  "content": "string"
}
```

### Interações com Postagens

#### Repostar ou Citar uma Postagem

- URL: `URLAPP/postings/posts/`
- Método: POST
- Formato JSON para Repostar:

```json
{
  "post_type": "repost",
  "original_post": "integer (ID da postagem)"
}
```

- Formato JSON para Citar:

```json
{
  "original_post": "integer (ID da postagem)",
  "content": "string",
  "post_type": "quote"
}
```

#### Curtir uma Postagem

- URL: `URLAPP/postings/posts/{POST_ID}/likes/`
- Método: POST

#### Comentar em uma Postagem

- URL: `URLAPP/postings/posts/{POST_ID}/comments/`
- Método: POST
- Campos JSON:

```json
{
  "content": "string"
}
```

#### Responder a um Comentário

- URL: `URLAPP/postings/posts/{POST_ID}/comments/{COMMENT_ID}/replies/`
- Método: POST
- Campos JSON:

```json
{
  "content": "string"
}
```

#### Curtir um Comentário

- URL: `URLAPP/postings/posts/{POST_ID}/comments/{COMMENT_ID}/likes/`
- Método: POST
