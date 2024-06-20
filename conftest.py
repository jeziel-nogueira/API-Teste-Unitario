""" import pytest
from app import create_app
from flask import Flask, jsonify
from flask_migrate import Migrate
from config import Config
from app.db import db
from app.auth import token_required, auth_bp


testpaths = "app/tests"
migrate = Migrate()

@pytest.fixture(scope="module")
def app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'SECRET_KEY'
    db.init_app(app)
    migrate.init_app(app, db)
    yield app

    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app """


import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"  # Use um banco de dados em memória para testes
    })

    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados de teste
        
        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
