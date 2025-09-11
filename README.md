# Wayne Industries - Sistema de Gerenciamento

Sistema web de gerenciamento de armamentos, veículos e itens, com controle de usuários e níveis de acesso.  

ESSE PROJETO FOI CRIADO SOMENTE PARA FINS ACADÊMICOS, REGISTRANDO A MINHA EVOLUÇÃO.
## 📌 Funcionalidades

### Dashboard
- Visualização das opções do sistema: Arsenal, Veículos, Itens e Perfil do usuário.
- Botão de logout.
- Boas-vindas personalizada com o nome do usuário.
- Controle de acesso: apenas administradores podem cadastrar novos usuários.

### Arsenal / Veículos / Itens
- CRUD completo: criar, editar, excluir e visualizar registros.
- Busca e filtro dinâmicos.
- Modal para cadastro e edição de registros.
- Cards estilizados para exibição dos itens.

### Perfil do Usuário
- Visualização de dados do usuário.
- Interface agradável e responsiva.

### Autenticação
- Login com validação de usuário e senha.
- Sessões mantidas com cookies.
- Mensagens de erro exibidas para tentativas incorretas.

---

## 💻 Tecnologias Utilizadas

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Banco de Dados:** SQLite
- **Bibliotecas:** Flask-CORS para integração frontend-backend
- **Controle de Sessão:** Flask session

---
⚡ Observações

- Controle de acesso: Apenas usuários com a role admin podem cadastrar novos usuários ou editar registros sensíveis.

- Banco SQLite: Certifique-se de que o arquivo de banco de dados não esteja aberto em outro programa para evitar erros de "database is locked".

- CORS: O backend permite requisições do frontend via Flask-CORS.

- Modal de cadastro/edição: Utilizado para criar e atualizar registros de forma dinâmica.
