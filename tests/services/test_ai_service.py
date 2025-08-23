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

def test_generate_timeout(ai_service):
    import requests
    with patch('services.ai_service.requests.post', side_effect=requests.Timeout()):
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

def test_send_chat_message_timeout(ai_service):
    import requests
    conversation = DummyConversation()
    with patch('services.ai_service.requests.post', side_effect=requests.Timeout()), \
         patch.object(ai_service, '_AIService__perform_similarity_search', return_value="context"):
        with pytest.raises(AIConnectionException):
            ai_service.send_chat_message("question", conversation)

def test_send_chat_message_similarity_search_error(ai_service):
    conversation = DummyConversation()
    with patch.object(ai_service, '_AIService__perform_similarity_search', side_effect=Exception("sim error")):
        with pytest.raises(AIConnectionException):
            ai_service.send_chat_message("question", conversation)

def test_output_streaming_response_generate(ai_service):
    mock_response = MagicMock()
    mock_response.iter_lines.return_value = [b'{"response": "Hello"}', b'{"response": " World"}']
    output = []
    def output_func(text):
        output.append(text)
    result = ai_service.output_streaming_response(mock_response, output_func, mode="generate")
    assert result == "Hello World"
    assert output[-1] == "Hello World"

def test_output_streaming_response_chat(ai_service):
    mock_response = MagicMock()
    mock_response.iter_lines.return_value = [b'{"message": {"content": "Hi"}}', b'{"message": {"content": " there"}}']
    output = []
    def output_func(text):
        output.append(text)
    result = ai_service.output_streaming_response(mock_response, output_func, mode="chat")
    assert result == "Hi there"
    assert output[-1] == "Hi there"

def test_generate_with_json_response(ai_service):
    with patch('services.ai_service.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "ok"}
        mock_post.return_value = mock_response
        response = ai_service.generate("prompt")
        assert response.json() == {"result": "ok"}

def test_generate_with_text_response(ai_service):
    with patch('services.ai_service.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "text response"
        mock_post.return_value = mock_response
        response = ai_service.generate("prompt")
        assert hasattr(response, "text")

def test_output_streaming_response_invalid_mode(ai_service):
    mock_response = MagicMock()
    mock_response.iter_lines.return_value = [b'{}']
    output = []
    def output_func(text):
        output.append(text)
    result = ai_service.output_streaming_response(mock_response, output_func, mode="invalid")
    assert result == ""

def test_output_streaming_response_malformed_json(ai_service):
    mock_response = MagicMock()
    mock_response.iter_lines.return_value = [b'{bad json']
    output = []
    def output_func(text):
        output.append(text)
    result = ai_service.output_streaming_response(mock_response, output_func, mode="generate")
    assert result == ""

def test_send_chat_message_no_context(ai_service):
    with patch('services.ai_service.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        conversation = DummyConversation()
        with patch.object(ai_service, '_AIService__perform_similarity_search', return_value=None):
            response = ai_service.send_chat_message("question", conversation)
            assert response == mock_response

def test_perform_similarity_search_success(ai_service):
    conversation = DummyConversation()
    with patch('services.ai_service.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": ["doc1", "doc2"]}
        mock_post.return_value = mock_response
        result = ai_service._AIService__perform_similarity_search("query", conversation)
        assert result == ["doc1", "doc2"]

def test_perform_similarity_search_failure(ai_service):
    conversation = DummyConversation()
    with patch('services.ai_service.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        with pytest.raises(AIEmbeddingException):
            ai_service._AIService__perform_similarity_search("query", conversation)

def test_perform_similarity_search_network_error(ai_service):
    conversation = DummyConversation()
    with patch('services.ai_service.requests.post', side_effect=Exception("network error")):
        with pytest.raises(AIConnectionException):
            ai_service._AIService__perform_similarity_search("query", conversation)
