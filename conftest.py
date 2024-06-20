import pytest
from app import create_app, db


# Criar instancia do app e db em memoria para teste
@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:" 
    })

    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados de teste
        
        yield app

        db.session.remove()
        db.drop_all()



# obter token de autenticaçao
@pytest.fixture()
def token(client):
    login_data = {
        'username': 'admin',
        'password': '123'
    }
    response = client.post('/auth/login', json=login_data)
    
    assert response.status_code == 200
    msg = response.get_json()

    token = msg.get('token')
    assert token is not None
    return token