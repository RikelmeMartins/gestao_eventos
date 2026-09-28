# 🎓 Gestão de Eventos Acadêmicos

Sistema web para organizar eventos acadêmicos (semanas acadêmicas, congressos, workshops e palestras), com cadastro de eventos e atividades, inscrições de participantes, controle de presença e emissão de certificados.

> 🚧 Projeto em desenvolvimento.

---

## 📋 Funcionalidades

- [x] Estrutura inicial do backend (API REST) e do frontend
- [ ] CRUD de eventos
- [ ] Cadastro e login de usuários (JWT)
- [ ] Cadastro de atividades (palestras, minicursos, oficinas)
- [ ] Inscrição em eventos e atividades com controle de vagas
- [ ] Check-in / registro de presença
- [ ] Emissão e validação de certificados em PDF
- [ ] Painel do organizador com relatórios

### Perfis de usuário

| Perfil | O que pode fazer |
|---|---|
| **Participante** | Ver eventos, se inscrever, baixar certificados |
| **Organizador** | Criar e gerenciar eventos, atividades e presenças |
| **Administrador** | Gerenciar usuários e todo o sistema |

---

## 🛠️ Tecnologias

**Backend**
- [Python 3.12+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/): API REST
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/): ORM
- [Flask-Migrate](https://flask-migrate.readthedocs.io/): migrations do banco
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/): autenticação
- [Flask-CORS](https://flask-cors.readthedocs.io/): comunicação com o frontend
- [psycopg](https://www.psycopg.org/): driver do PostgreSQL

**Frontend**
- [React](https://react.dev/) + [Vite](https://vitejs.dev/)
- [React Router](https://reactrouter.com/): navegação entre páginas
- [Axios](https://axios-http.com/): requisições à API
- HTML, CSS e JavaScript

**Banco de dados**
- [PostgreSQL](https://www.postgresql.org/)

---

## 📁 Estrutura do projeto

```
gestao_eventos/
├── backend/
│   ├── app/
│   │   ├── __init__.py      # create_app() – fábrica da aplicação
│   │   ├── extensions.py    # db, migrate, jwt, cors
│   │   ├── models/          # tabelas do banco
│   │   ├── schemas/         # validação / serialização
│   │   ├── routes/          # endpoints da API (Blueprints)
│   │   └── services/        # regras de negócio
│   ├── migrations/          # histórico do banco (Flask-Migrate)
│   ├── tests/
│   ├── .env                 # variáveis de ambiente (não versionado)
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── src/
│   │   ├── components/      # componentes reutilizáveis
│   │   ├── pages/           # telas do sistema
│   │   ├── services/        # configuração do axios / chamadas à API
│   │   ├── context/         # estado global (ex.: usuário logado)
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
├── .gitignore
└── README.md
```

---

## 🚀 Como rodar o projeto

### Pré-requisitos

- [Python 3.12+](https://www.python.org/downloads/)
- [Node.js LTS](https://nodejs.org/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Git](https://git-scm.com/)

### 1. Clonar o repositório

```bash
git clone https://github.com/RikelmeMartins/gestao_eventos.git
cd gestao_eventos
```

### 2. Criar o banco de dados

No pgAdmin (ou no `psql`), crie um banco chamado `eventos_db`:

```sql
CREATE DATABASE eventos_db;
```

### 3. Backend

```bash
cd backend

# criar e ativar o ambiente virtual
python -m venv .venv
source .venv/Scripts/activate      # Windows (Git Bash)
# .venv\Scripts\activate           # Windows (PowerShell / CMD)
# source .venv/bin/activate        # Linux / Mac

# instalar dependências
pip install -r requirements.txt
```

Crie o arquivo `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:SUA_SENHA@localhost:5432/eventos_db
JWT_SECRET_KEY=troque-por-uma-chave-secreta
```

Crie as tabelas e inicie o servidor:

```bash
flask --app run db upgrade
python run.py
```

A API ficará disponível em **http://localhost:5000**.

### 4. Frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

O sistema abrirá em **http://localhost:5173**.

---

## 🔌 Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/eventos/` | Lista todos os eventos |
| `POST` | `/api/eventos/` | Cria um novo evento |
| `GET` | `/api/eventos/<id>` | Detalhes de um evento *(em breve)* |
| `PUT` | `/api/eventos/<id>` | Atualiza um evento *(em breve)* |
| `DELETE` | `/api/eventos/<id>` | Remove um evento *(em breve)* |
| `POST` | `/api/auth/register` | Cadastro de usuário *(em breve)* |
| `POST` | `/api/auth/login` | Login e geração de token *(em breve)* |

Exemplo de criação de evento:

```json
POST /api/eventos/
{
  "titulo": "Semana Acadêmica de Computação",
  "descricao": "Palestras e minicursos sobre tecnologia",
  "data_inicio": "2026-10-20T08:00:00",
  "data_fim": "2026-10-24T18:00:00",
  "local": "Auditório Central",
  "vagas": 200
}
```

---

## 🗃️ Comandos úteis

```bash
# Backend: após criar ou alterar um model
flask --app run db migrate -m "descrição da mudança"
flask --app run db upgrade

# Backend: atualizar a lista de dependências
pip freeze > requirements.txt

# Frontend: gerar a versão de produção
npm run build
```

---

## 👤 Autor

**Rikelme Martins**
[GitHub](https://github.com/RikelmeMartins)
