import requests
import json

# URL base da API
BASE_URL = "http://flask:5000"

def test_cadastrar_aluno():
    """
    Testa o cadastro de um aluno na API.
    """
    url = f"{BASE_URL}/alunos"
    headers = {"Content-Type": "application/json"}
    payload = {
        "nome": "Teste",
        "sobrenome": "Usuario",
        "turma": "101",
        "disciplinas": "Matematica,Fisica"
    }

    # Envia o POST para cadastrar o aluno
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Verifica se o aluno foi criado com sucesso
    assert response.status_code == 201, f"Erro ao cadastrar aluno: {response.text}"
    print("Teste de cadastro de aluno: SUCESSO")

    # Busca todos os alunos para verificar o registro
    response_get = requests.get(url)
    assert response_get.status_code == 200, f"Erro ao buscar alunos: {response_get.text}"
    alunos = response_get.json()

    # Verifica se o aluno recém-criado está na lista
    assert any(
        aluno['nome'] == payload['nome'] and aluno['sobrenome'] == payload['sobrenome']
        for aluno in alunos
    ), "Aluno recém-criado não encontrado na lista."
    print("Aluno criado com sucesso está presente na lista.")

if __name__ == "__main__":
    test_cadastrar_aluno()
