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
  "email": "string",
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

- URL: `URLAPP/accounts/users/{USER_ID|USERNAME}/`
- Método: GET

#### Detalhes do Usuário Ativo

- URL: `URLAPP/accounts/users/me/`
- Método: GET
- Necessita Token Jwt

#### Listagem de seguidores

- URL: `URLAPP/accounts/users/{USER_ID}/followers/`
- Método: GET

#### Listagem de seguindo

- URL: `URLAPP/accounts/users/{USER_ID}/following/`
- Método: GET

#### Listagem de recomendações para seguir

- URL: `URLAPP/accounts/users/{USER_ID}/recommendations/`
- Método: GET

#### Postagens de um usuário

- URL: `URLAPP/accounts/users/{USER_ID|USERNAME}/posts/`
- Método: GET

#### Pesquisar Usuários

- URL: `URLAPP/accounts/users/search/?q={DATA_SEARCH}`
- Método: PUT/PATCH
- Formato JSON:

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
  "name": "string (opcional)",
  "username": "string (opcional)",
  "email": "string (opcional)",
  "password": "string (opcional)",
  "old_password": "string (obrigatório para alteração de senha)",
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
Os comentários são tratados como um tipo de postagem.

#### Lista de Postagens

- URL: `URLAPP/postings/posts/`
- Método: GET

#### Feed de um usuário

- URL: `URLAPP/postings/feed/`
- Método: GET

#### Lista de Likes de uma postagem

- URL: `URLAPP/postings/posts/{POST_ID}/likes/`
- Método: GET

#### Lista de Comentários de uma postagem

- URL: `URLAPP/postings/posts/{POST_ID}/comments/`
- Método: GET

#### Lista de Citações e Repostagens de uma postagem

- URL: `URLAPP/postings/posts/{POST_ID}/quotes/`
- URL: `URLAPP/postings/posts/{POST_ID}/reposts/`
- Método: GET

#### Criação de Postagem

- URL: `URLAPP/postings/posts/`
- Método: POST
- Campos JSON:

```json
{
  "post_type": "(comment, original, quote ou repost)",
  "content": "string",
  "original_post": "(Obrigatório para postagens que não são originais)"
}
```

### Interações com Postagens e Comentários

#### Repostar ou Citar

- URL: `URLAPP/postings/posts/`
- Método: POST
- Formato JSON para Repostar:

```json
{
  "post_type": "repost",
  "original_post": "id do post original"
}
```

- Formato JSON para Citar:

```json
{
  "post_type": "quote",
  "original_post": "id do post original",
  "content": "string"
}
```

#### Curtir

- URL: `URLAPP/postings/posts/{POST_ID}/likes/`
- Método: POST

#### Comentar

- URL: `URLAPP/postings/posts/{POST_ID}/comments/`
- Método: POST
- Campos JSON:

```json
{
  "content": "string"
}
```
