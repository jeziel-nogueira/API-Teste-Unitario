from flask import jsonify, request
from conftest import app

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
    print(msg)
    
    # Adicione mais verificações conforme necessário
    assert msg.get('message') == 'Login successful'


""" 
def test_app_login(app):
    #response = app.get('/login')
    response = app().get('/login')
    res = response.request.get_json()# jsonify.get .loads(response.data.decode('utf-8')).get("Books")
    print(res)
    assert res.status_code == 400
    assert type(res) == dict """