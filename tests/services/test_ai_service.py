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
        with pytest.raises(AIConnectionException):
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


def test_perform_similarity_search_network_error(ai_service):
    mock_vector_store = MagicMock()
    mock_vector_store.similarity_search.side_effect = Exception("network error")
    with pytest.raises(Exception):
        ai_service._AIService__perform_similarity_search("query", mock_vector_store, 5)

def test_perform_similarity_search_empty(ai_service):
    mock_vector_store = MagicMock()
    mock_vector_store.similarity_search.return_value = []
    result = ai_service._AIService__perform_similarity_search("query", mock_vector_store, top_k=2)
    assert result == ""

def test_perform_similarity_search_exception(ai_service):
    mock_vector_store = MagicMock()
    mock_vector_store.similarity_search.side_effect = Exception("fail")
    with pytest.raises(Exception):
        ai_service._AIService__perform_similarity_search("query", mock_vector_store, top_k=2)

def test_get_vector_store_success(ai_service):
    with patch("services.ai_service.FAISS.from_texts") as mock_from_texts:
        mock_vs = MagicMock()
        mock_from_texts.return_value = mock_vs
        result = ai_service.get_vector_store(["a", "b"])
        assert result == mock_vs

def test_get_vector_store_save_error(ai_service):
    with patch("services.ai_service.FAISS.from_texts") as mock_from_texts:
        mock_vs = MagicMock()
        mock_vs.save_local.side_effect = Exception("fail")
        mock_from_texts.return_value = mock_vs
        with pytest.raises(AIEmbeddingException):
            ai_service.get_vector_store(["a"], embedding_path="/tmp/path")

def test_get_vector_store_embed_error(ai_service):
    with patch("services.ai_service.FAISS.from_texts", side_effect=Exception("fail")):
        with pytest.raises(AIEmbeddingException):
            ai_service.get_vector_store(["a"])

def test_load_vector_store_from_path_success(ai_service):
    with patch("services.ai_service.FAISS.load_local") as mock_load:
        mock_vs = MagicMock()
        mock_load.return_value = mock_vs
        result = ai_service.load_vector_store_from_path("/tmp/path")
        assert result == mock_vs

def test_load_vector_store_from_path_error(ai_service):
    with patch("services.ai_service.FAISS.load_local", side_effect=Exception("fail")):
        with pytest.raises(AIEmbeddingException):
            ai_service.load_vector_store_from_path("/tmp/path")

def test_merge_vector_stores_empty(ai_service):
    with pytest.raises(AIEmbeddingException):
        ai_service.merge_vector_stores([])

def test_merge_vector_stores_single(ai_service):
    mock_vs = MagicMock()
    result = ai_service.merge_vector_stores([mock_vs])
    assert result == mock_vs

def test_merge_vector_stores_merge_error(ai_service):
    mock_vs1 = MagicMock()
    mock_vs2 = MagicMock()
    mock_vs1.merge_from.side_effect = Exception("fail")
    with pytest.raises(AIEmbeddingException):
        ai_service.merge_vector_stores([mock_vs1, mock_vs2])

def test_merge_vector_stores_success(ai_service):
    mock_vs1 = MagicMock()
    mock_vs2 = MagicMock()
    mock_vs1.merge_from = MagicMock()
    result = ai_service.merge_vector_stores([mock_vs1, mock_vs2])
    mock_vs1.merge_from.assert_called_with(mock_vs2)
    assert result == mock_vs1

def test_generate_conversation_name_success(ai_service):
    conversation = MagicMock()
    conversation.get_messages.return_value = ["msg1", "msg2"]
    conversation.document_ids = [1, 2]
    with patch("database.repository.document_repository.DocumentRepository.get_bibtex_by_document_id", return_value="@article{foo}"):
        with patch.object(ai_service, "generate") as mock_generate, \
             patch.object(ai_service, "output_streaming_response", return_value="title") as mock_output:
            mock_generate.return_value = MagicMock()
            result = ai_service.generate_conversation_name(conversation)
            assert result == "title"

def test_generate_conversation_name_error(ai_service):
    conversation = MagicMock()
    conversation.get_messages.return_value = ["msg1"]
    conversation.document_ids = [1]
    with patch("database.repository.document_repository.DocumentRepository.get_bibtex_by_document_id", return_value="@article{foo}"):
        with patch.object(ai_service, "generate", side_effect=Exception("fail")):
            with pytest.raises(AIConnectionException):
                ai_service.generate_conversation_name(conversation)




