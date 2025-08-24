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
    from unittest.mock import MagicMock
    mock_auth0 = MagicMock()
    mock_auth0.authorize_redirect.return_value = 'redirected'
    auth_service.oauth.auth0 = mock_auth0
    with patch('services.user_management.authentication_service.url_for', return_value='/callback'):
        result = auth_service.login()
        assert result == 'redirected'
        mock_auth0.authorize_redirect.assert_called_once()

def test_callback_success(auth_service, app):
    from unittest.mock import MagicMock
    mock_auth0 = MagicMock()
    mock_auth0.authorize_access_token.return_value = {
        'userinfo': {
            'sub': 'auth0|123',
            'given_name': 'John',
            'family_name': 'Doe',
            'email': 'john@example.com'
        }
    }
    auth_service.oauth.auth0 = mock_auth0
    with app.test_request_context():
        with patch('services.user_management.authentication_service.UserRepository.save'), \
             patch('services.user_management.authentication_service.UserRepository.activate_user'), \
             patch('services.user_management.authentication_service.redirect', return_value='redirected') as mock_redirect:
            result = auth_service.callback()
            assert result == 'redirected'

def test_callback_error(auth_service, app):
    from unittest.mock import MagicMock
    mock_auth0 = MagicMock()
    mock_auth0.authorize_access_token.side_effect = Exception('fail')
    auth_service.oauth.auth0 = mock_auth0
    with app.test_request_context():
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

def test_init_oauth_missing_env(auth_service, app, monkeypatch):
    monkeypatch.setenv('AUTH0_CLIENT_ID', '')
    monkeypatch.setenv('AUTH0_CLIENT_SECRET', '')
    monkeypatch.setenv('AUTH0_DOMAIN', '')
    with patch.object(auth_service.oauth, 'init_app') as mock_init_app, \
         patch.object(auth_service.oauth, 'register') as mock_register:
        auth_service.init_oauth(app)
        mock_init_app.assert_called_once_with(app)
        mock_register.assert_called_once()
        args, kwargs = mock_register.call_args
        assert kwargs['client_id'] == ''
        assert kwargs['client_secret'] == ''
        assert kwargs['server_metadata_url'] == 'https:///.well-known/openid-configuration'

def test_login_missing_auth0(auth_service):
    auth_service.oauth.auth0 = None
    with patch('services.user_management.authentication_service.url_for', return_value='/callback'):
        try:
            auth_service.login()
        except AttributeError:
            assert True
        else:
            assert False

def test_callback_missing_userinfo(auth_service, app):
    with app.test_request_context():
        with patch.object(auth_service.oauth.auth0, 'authorize_access_token', return_value={}), \
             patch('services.user_management.authentication_service.redirect', return_value='redirected') as mock_redirect:
            result = auth_service.callback()
            assert result == 'redirected'
            mock_redirect.assert_called_once()

def test_callback_userrepo_save_error(auth_service, app):
    with app.test_request_context():
        with patch.object(auth_service.oauth.auth0, 'authorize_access_token', return_value={'userinfo': {'sub': 'auth0|123'}}), \
             patch('services.user_management.authentication_service.UserRepository.save', side_effect=Exception('fail')), \
             patch('services.user_management.authentication_service.redirect', return_value='redirected') as mock_redirect:
            result = auth_service.callback()
            assert result == 'redirected'
            mock_redirect.assert_called_once()

def test_logout_empty_session(auth_service, app):
    with app.test_request_context():
        with patch('services.user_management.authentication_service.session.clear') as mock_clear, \
             patch('services.user_management.authentication_service.redirect', return_value='redirected') as mock_redirect:
            # session is empty
            result = auth_service.logout()
            assert result == 'redirected'
            mock_clear.assert_called_once()

def test_get_user_verification_missing_keys(auth_service, app):
    with app.test_request_context():
        with patch('services.user_management.authentication_service.session', {'user': {}}):
            resp, code = auth_service.get_user_verification()
            assert code == 401
            assert resp.json['user-verification'] is False

def test_get_user_verification_viewmode_error(auth_service, app):
    with app.test_request_context():
        with patch('services.user_management.authentication_service.session', dict(user={'userinfo': {'sub': 'auth0|123', 'picture': 'pic', 'given_name': 'John'}})), \
             patch.object(auth_service.user_repository, 'get_view_mode', side_effect=Exception('fail')):
            resp, code = auth_service.get_user_verification()
            assert code == 500
            assert resp.json['user-verification'] is False