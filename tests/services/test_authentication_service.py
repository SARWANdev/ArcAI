import pytest
from unittest.mock import patch
from flask import Flask
from services.user_management.authentication_service import AuthenticationService

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test'
    return app

@pytest.fixture
def auth_service(app):
    return AuthenticationService(app)

def test_init_oauth_registers_auth0(auth_service, app):
    with patch.object(auth_service.oauth, 'init_app') as mock_init_app, \
         patch.object(auth_service.oauth, 'register') as mock_register:
        auth_service.init_oauth(app)
        mock_init_app.assert_called_once_with(app)
        mock_register.assert_called_once()

def test_login_redirect(auth_service):
    with patch.object(auth_service.oauth.auth0, 'authorize_redirect', return_value='redirected') as mock_auth:
        with patch('services.user_management.authentication_service.url_for', return_value='/callback'):
            result = auth_service.login()
            assert result == 'redirected'
            mock_auth.assert_called_once()

def test_callback_success(auth_service, app):
    with app.test_request_context():
        with patch.object(auth_service.oauth.auth0, 'authorize_access_token', return_value={'userinfo': {'sub': 'auth0|123', 'given_name': 'John', 'family_name': 'Doe', 'email': 'john@example.com'}}), \
             patch('services.user_management.authentication_service.UserRepository.save'), \
             patch('services.user_management.authentication_service.UserRepository.activate_user'), \
             patch('services.user_management.authentication_service.redirect', return_value='redirected') as mock_redirect:
            result = auth_service.callback()
            assert result == 'redirected'

def test_callback_error(auth_service, app):
    with app.test_request_context():
        with patch.object(auth_service.oauth.auth0, 'authorize_access_token', side_effect=Exception('fail')):
            result, code = auth_service.callback()
            assert code == 400
            assert 'error' in result.json

def test_get_user_verification_authenticated(auth_service, app):
    with app.test_request_context():
        with patch('services.user_management.authentication_service.session', dict(user={'userinfo': {'sub': 'auth0|123', 'picture': 'pic', 'given_name': 'John'}})), \
             patch.object(auth_service.user_repository, 'get_view_mode', return_value=True):
            resp, code = auth_service.get_user_verification()
            assert code == 200
            assert resp.json['user-verification'] is True
            assert resp.json['name'] == 'John'

def test_get_user_verification_unauthenticated(auth_service, app):
    with app.test_request_context():
        with patch('services.user_management.authentication_service.session', {}):
            resp, code = auth_service.get_user_verification()
            assert code == 401
            assert resp.json['user-verification'] is False

def test_logout(auth_service, app):
    with app.test_request_context():
        with patch('services.user_management.authentication_service.session.clear') as mock_clear, \
             patch('services.user_management.authentication_service.redirect', return_value='redirected') as mock_redirect:
            result = auth_service.logout()
            assert result == 'redirected'
            mock_clear.assert_called_once()
