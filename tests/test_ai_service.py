import pytest
from unittest.mock import patch, MagicMock
from services.ai_service import AIService
from exceptions.ai_exceptions import AIConnectionException, AIGenerationException, AIEmbeddingException

class DummyConversation:
    def get_vector_store(self):
        return MagicMock()
    def format_last_user_message(self, context=None):
        return ["user message"]

@pytest.fixture
def ai_service():
    return AIService(base_url="http://testserver", llm_name="test-llm", embedding_model_name="test-embed")

def test_generate_success(ai_service):
    with patch('services.ai_service.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        response = ai_service.generate("test prompt")
        assert response == mock_response

def test_generate_failure(ai_service):
    with patch('services.ai_service.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        with pytest.raises(AIGenerationException):
            ai_service.generate("test prompt")

def test_generate_network_error(ai_service):
    with patch('services.ai_service.requests.post', side_effect=Exception("network error")):
        with pytest.raises(AIConnectionException):
            ai_service.generate("test prompt")

def test_send_chat_message_success(ai_service):
    with patch('services.ai_service.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        conversation = DummyConversation()
        with patch.object(ai_service, '_AIService__perform_similarity_search', return_value="context"):
            response = ai_service.send_chat_message("question", conversation)
            assert response == mock_response

def test_send_chat_message_failure(ai_service):
    with patch('services.ai_service.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        conversation = DummyConversation()
        with patch.object(ai_service, '_AIService__perform_similarity_search', return_value="context"):
            with pytest.raises(AIGenerationException):
                ai_service.send_chat_message("question", conversation)

def test_send_chat_message_network_error(ai_service):
    with patch('services.ai_service.requests.post', side_effect=Exception("network error")):
        conversation = DummyConversation()
        with patch.object(ai_service, '_AIService__perform_similarity_search', return_value="context"):
            with pytest.raises(AIConnectionException):
                ai_service.send_chat_message("question", conversation)
