def test_app_incorrect_login(client):
    # Dados de login e senha a serem enviados no payload JSON
    login_data = {
        'username': 'admn',
        'password': '123'
    }
    
    # Enviar a requisição POST com o payload JSON
    response = client.post('/auth/login', json=login_data)
    
    # Verificar se a resposta é 200 OK
    assert response.status_code == 401
    msg = response.get_json()
    
    assert msg.get('message') == 'Invalid usernameo or password'


def test_app_login(client):
    # Dados de login e senha a serem enviados no payload JSON
    login_data = {
        'username': 'admin',
        'password': '123'
    }
    
    # Enviar a requisição POST com o payload JSON
    response = client.post('/auth/login', json=login_data)
    
    # Verificar se a resposta é 200 OK
    assert response.status_code == 200
    msg = response.get_json()

    token = msg.get('token')
    assert token is not None
    
    assert msg.get('message') == 'Login successful'

def test_app_create_client(client, token):
    
    # dados de auth para area protegida por login
    header = {
        'x-access-token': token,
        'Content-Type': 'application/json'
    }

    #payload para cadastrar novo cliente
    data = {
        "name": "Fe",
        "email": "@Fe"
    }
    protected = client.post('/clients', headers = header, json=data)
    #print("Header:", header)
    #print("Status Code:", protected.status_code)
    #print("Body:", protected.get_json())
    assert protected.status_code == 201

def test_get_all_user(client, token):

    # add novo cliente
    # dados de auth para area protegida por login
    header = {
        'x-access-token': token,
        'Content-Type': 'application/json'
    }

    #payload para cadastrar novo cliente
    data = {
        "name": "Jao",
        "email": "@Jao"
    }
    protected = client.post('/clients', headers = header, json=data)

    #payload vazio para listar todos
    data = {
    }
    protected = client.get('/clients', headers = header, json=data)
    """ print("Header:", header)
    print("Response Status Code:", protected.status_code)
    print("Response Body:", protected.get_json()) """

    res = protected.get_json()
    print(res)

    assert len(res) == 2
    assert protected.status_code == 200

def test_get_user_by_id(client, token):
    
    # dados de auth para area protegida por login
    header = {
        'x-access-token': token,
        'Content-Type': 'application/json'
    }
    data = {
        "client_id":1
    }
    protected = client.get('/clients', headers = header, json=data)
    """ print("Header:", header)
    print("Response Status Code:", protected.status_code)
    print("Response Body:", protected.get_json()) """

    res = protected.get_json()
    #print(type(res))
    print(res)

    #first_client = res[0]
    #print(first_client)

    assert res.get('id') == 1
    assert res.get('name') == "Fe"
    assert res.get('email') == "@Fe"
    assert protected.status_code == 200



def test_update_client(client, token):

    # add novo cliente
    # dados de auth para area protegida por login
    header = {
        'x-access-token': token,
        'Content-Type': 'application/json'
    }

    #payload pro Jao q trocou de nome
    data = {
        "id":2,
        "name": "Joca",
        "email": "@Joca"
    }
    protected = client.put('/clients', headers = header, json=data)

    #print("Response Status Code:", protected.status_code)
    #print("Response Body:", protected.get_json())

    res = protected.get_json()
    #print(res)
    
    #a mensagem de conf é o segundo elemento da lista, index = 1
    assert res[1].get('message') == 'Client updated'
    assert protected.status_code == 200



def test_delete_client(client, token):
    header = {
        'x-access-token': token,
        'Content-Type': 'application/json'
    }

    #payload pro Jao q desistiu de tudo
    data = {
        "id":2
    }
    protected = client.delete('/clients', headers = header, json=data)

    assert protected.status_code == 204 # status_code 204 => nao possui corpo de resposta


def test_if_deleted(client, token):
     # dados de auth para area protegida por login
    header = {
        'x-access-token': token,
        'Content-Type': 'application/json'
    }
    data = {
        "client_id":2
    }
    protected = client.get('/clients', headers = header, json=data)
    #print("Header:", header)
    #print("Response Status Code:", protected.status_code)
    print("Response Body:", protected.get_json())

    res = protected.get_json()
    print(type(res))
    print(res.get('message'))

    assert protected.status_code == 500
    assert res.get('message') == 'Client id not found'