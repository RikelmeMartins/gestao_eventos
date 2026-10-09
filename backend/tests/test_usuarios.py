URL = "/api/usuarios/"

USUARIO = {
    "nome": "Maria Silva",
    "email": "maria@exemplo.com",
    "senha": "segredo123",
}


def cadastrar(client, **extra):
    resp = client.post(URL, json={**USUARIO, **extra})
    assert resp.status_code == 201
    return resp.get_json()


def test_cadastrar_e_detalhar(client):
    usuario = cadastrar(client)
    assert usuario == {"id": 1, "nome": "Maria Silva", "email": "maria@exemplo.com", "perfil": "participante"}

    resp = client.get(f"{URL}{usuario['id']}")
    assert resp.status_code == 200
    assert resp.get_json() == usuario


def test_resposta_nao_expoe_senha(client):
    usuario = cadastrar(client)
    assert "senha" not in usuario
    assert "senha_hash" not in usuario


def test_perfil_enviado_pelo_cliente_e_rejeitado(client):
    resp = client.post(URL, json={**USUARIO, "perfil": "admin"})
    assert resp.status_code == 400


def test_email_duplicado(client):
    cadastrar(client)
    resp = client.post(URL, json={**USUARIO, "email": "MARIA@exemplo.com"})
    assert resp.status_code == 409


def test_dados_invalidos(client):
    resp = client.post(URL, json={"nome": "", "email": "nao-e-email", "senha": "123"})
    assert resp.status_code == 400
    assert set(resp.get_json()["detalhes"]) == {"nome", "email", "senha"}


def test_listar(client):
    cadastrar(client)
    cadastrar(client, nome="Ana", email="ana@exemplo.com")
    nomes = [u["nome"] for u in client.get(URL).get_json()]
    assert nomes == ["Ana", "Maria Silva"]


def test_usuario_inexistente(client):
    resp = client.get(f"{URL}999")
    assert resp.status_code == 404


def test_login(client):
    cadastrar(client)
    resp = client.post(f"{URL}login", json={"email": USUARIO["email"], "senha": USUARIO["senha"]})
    assert resp.status_code == 200
    corpo = resp.get_json()
    assert corpo["access_token"]
    assert corpo["usuario"]["email"] == USUARIO["email"]


def test_login_senha_errada(client):
    cadastrar(client)
    resp = client.post(f"{URL}login", json={"email": USUARIO["email"], "senha": "errada"})
    assert resp.status_code == 401
