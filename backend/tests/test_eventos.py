URL = "/api/eventos/"

EVENTO = {
    "titulo": "Semana Acadêmica de Computação",
    "descricao": "Palestras e minicursos",
    "data_inicio": "2026-11-10T08:00:00",
    "data_fim": "2026-11-14T18:00:00",
    "local": "Auditório Central",
    "vagas": 200,
}


def criar(client, **extra):
    resp = client.post(URL, json={**EVENTO, **extra})
    assert resp.status_code == 201
    return resp.get_json()


def test_criar_e_detalhar(client):
    evento = criar(client)
    assert evento["id"] == 1
    assert evento["titulo"] == EVENTO["titulo"]

    resp = client.get(f"{URL}{evento['id']}")
    assert resp.status_code == 200
    assert resp.get_json() == evento


def test_listar_ordenado_por_data(client):
    criar(client, titulo="Depois", data_inicio="2026-12-01T08:00:00", data_fim="2026-12-01T12:00:00")
    criar(client, titulo="Antes")

    titulos = [e["titulo"] for e in client.get(URL).get_json()]
    assert titulos == ["Antes", "Depois"]


def test_criar_sem_campos_obrigatorios(client):
    resp = client.post(URL, json={"local": "Sala 1"})
    assert resp.status_code == 400
    detalhes = resp.get_json()["detalhes"]
    assert {"titulo", "data_inicio", "data_fim"} <= detalhes.keys()


def test_criar_com_data_fim_antes_do_inicio(client):
    resp = client.post(URL, json={**EVENTO, "data_fim": "2026-11-01T08:00:00"})
    assert resp.status_code == 400
    assert "data_fim" in resp.get_json()["detalhes"]


def test_criar_com_vagas_negativas(client):
    resp = client.post(URL, json={**EVENTO, "vagas": -1})
    assert resp.status_code == 400


def test_criar_com_campo_desconhecido(client):
    resp = client.post(URL, json={**EVENTO, "id": 99})
    assert resp.status_code == 400


def test_patch_altera_so_o_enviado(client):
    evento = criar(client)
    resp = client.patch(f"{URL}{evento['id']}", json={"local": "Bloco B"})
    assert resp.status_code == 200
    dados = resp.get_json()
    assert dados["local"] == "Bloco B"
    assert dados["titulo"] == EVENTO["titulo"]


def test_patch_valida_datas_com_os_valores_atuais(client):
    evento = criar(client)
    resp = client.patch(f"{URL}{evento['id']}", json={"data_fim": "2026-11-01T08:00:00"})
    assert resp.status_code == 400


def test_put_exige_evento_completo(client):
    evento = criar(client)
    resp = client.put(f"{URL}{evento['id']}", json={"titulo": "Só o título"})
    assert resp.status_code == 400

    resp = client.put(f"{URL}{evento['id']}", json={**EVENTO, "titulo": "Novo título"})
    assert resp.status_code == 200
    assert resp.get_json()["titulo"] == "Novo título"


def test_excluir(client):
    evento = criar(client)
    assert client.delete(f"{URL}{evento['id']}").status_code == 204
    assert client.get(f"{URL}{evento['id']}").status_code == 404


def test_evento_inexistente_retorna_404_em_json(client):
    for metodo in (client.get, client.patch, client.put, client.delete):
        resp = metodo(f"{URL}999", json={})
        assert resp.status_code == 404
        assert resp.get_json() == {"erro": "Evento não encontrado."}
