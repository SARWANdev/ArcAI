import pytest
from unittest.mock import patch, MagicMock, mock_open, ANY
from services.upload_manager import hash_manager, embeddings_manager, server_conection
import io

# hash_manager tests
def test_get_pdf_sha256(tmp_path):
    file_path = tmp_path / "test.pdf"
    file_path.write_bytes(b"test content")
    result = hash_manager.get_pdf_sha256(str(file_path))
    import hashlib
    expected = hashlib.sha256(b"test content").hexdigest()
    assert result == expected

def test_get_pdf_sha256_file_not_found():
    with pytest.raises(FileNotFoundError):
        hash_manager.get_pdf_sha256("nonexistent.pdf")

def test_relative_path_generator():
    assert hash_manager.relative_path_generator("user1", "proj1") == "user1/proj1"

# embeddings_manager tests
def test_serialize_vector_store():
    mock_faiss = MagicMock()
    with patch("tempfile.TemporaryDirectory") as mock_tempdir:
        mock_dir = mock_tempdir.return_value.__enter__.return_value
        with patch("builtins.open", mock_open(read_data=b"data")):
            result = embeddings_manager.EmbeddingsManager.serialize_vector_store(mock_faiss)
            assert isinstance(result, tuple)
            assert isinstance(result[0], io.BytesIO)
            assert isinstance(result[1], io.BytesIO)

def test_serialize_vector_store_ioerror():
    mock_faiss = MagicMock()
    with patch("tempfile.TemporaryDirectory") as mock_tempdir:
        mock_dir = mock_tempdir.return_value.__enter__.return_value
        with patch("builtins.open", side_effect=IOError("fail")):
            with pytest.raises(IOError):
                embeddings_manager.EmbeddingsManager.serialize_vector_store(mock_faiss)

def test_load_remote_faiss_index():
    with patch("tempfile.TemporaryDirectory") as mock_tempdir, \
         patch("services.upload_manager.embeddings_manager.ssh_connection") as mock_ssh, \
         patch("services.upload_manager.embeddings_manager.AIService.load_vector_store_from_path", return_value="faiss") as mock_load:
        mock_dir = mock_tempdir.return_value.__enter__.return_value
        mock_sftp = MagicMock()
        mock_ssh_inst = MagicMock()
        mock_ssh.return_value = mock_ssh_inst
        mock_ssh_inst.open_sftp.return_value = mock_sftp
        mock_sftp.get = MagicMock()
        result = embeddings_manager.EmbeddingsManager.load_remote_faiss_index("/remote/path")
        assert result == "faiss"
        mock_sftp.get.assert_any_call('/remote/path/index.faiss', ANY)
        mock_sftp.get.assert_any_call('/remote/path/index.pkl', ANY)

def test_get_embeddings():
    with patch("services.upload_manager.embeddings_manager.DocumentRepository.get_path", return_value="/tmp/doc1"), \
         patch.object(embeddings_manager.EmbeddingsManager, "load_remote_faiss_index", return_value="embedding"):
        result = embeddings_manager.EmbeddingsManager.get_embeddings(["doc1"])
        assert result == ["embedding"]

def test_get_embeddings_empty():
    with patch("services.upload_manager.embeddings_manager.DocumentRepository.get_path", return_value=None), \
         patch.object(embeddings_manager.EmbeddingsManager, "load_remote_faiss_index", return_value=None):
        result = embeddings_manager.EmbeddingsManager.get_embeddings([])
        assert result == []

# server_conection tests
def test_save_document_content():
    with patch("services.upload_manager.server_conection.ssh_connection") as mock_ssh:
        mock_sftp = MagicMock()
        mock_ssh_inst = MagicMock()
        mock_ssh.return_value = mock_ssh_inst
        mock_ssh_inst.open_sftp.return_value = mock_sftp
        mock_file = mock_sftp.file.return_value.__enter__.return_value
        result = server_conection.save_document_content("/remote/file", b"data")
        mock_file.write.assert_called_once_with(b"data")
        assert result is True

def test_save_document_content_error():
    with patch("services.upload_manager.server_conection.ssh_connection", side_effect=Exception("fail")):
        result = server_conection.save_document_content("/remote/file", b"data")
        assert result is False

def test_retrieve_document_content():
    with patch("services.upload_manager.server_conection.ssh_connection") as mock_ssh:
        mock_sftp = MagicMock()
        mock_ssh_inst = MagicMock()
        mock_ssh.return_value = mock_ssh_inst
        mock_ssh_inst.open_sftp.return_value = mock_sftp
        mock_file = mock_sftp.file.return_value.__enter__.return_value
        mock_file.read.return_value = b"data"
        result = server_conection.retrieve_document_content("/remote/file")
        assert result == b"data"

def test_retrieve_document_content_error():
    with patch("services.upload_manager.server_conection.ssh_connection", side_effect=Exception("fail")):
        result = server_conection.retrieve_document_content("/remote/file")
        assert result is None

def test_delete_remote_directory():
    with patch("services.upload_manager.server_conection.ssh_connection") as mock_ssh:
        mock_ssh_inst = MagicMock()
        mock_ssh.return_value = mock_ssh_inst
        mock_ssh_inst.exec_command.return_value = (None, MagicMock(channel=MagicMock(recv_exit_status=MagicMock(return_value=0))), MagicMock(read=MagicMock(return_value=b"")))
        result = server_conection.delete_remote_directory("/remote/dir")
        assert result is True

def test_delete_remote_directory_error():
    with patch("services.upload_manager.server_conection.ssh_connection", side_effect=Exception("fail")):
        result = server_conection.delete_remote_directory("/remote/dir")
        assert result is False

def test_delete_remote_directory_if_empty():
    with patch("services.upload_manager.server_conection.ssh_connection") as mock_ssh:
        mock_ssh_inst = MagicMock()
        mock_ssh.return_value = mock_ssh_inst
        # Simulate empty dir
        mock_ssh_inst.exec_command.side_effect = [
            (None, MagicMock(read=MagicMock(return_value=b"EMPTY")), None),
            (None, MagicMock(channel=MagicMock(recv_exit_status=MagicMock(return_value=0))), MagicMock(read=MagicMock(return_value=b"")))
        ]
        result = server_conection.delete_remote_directory_if_empty("/remote/dir/file.pdf")
        assert result is True

def test_delete_remote_directory_if_empty_error():
    with patch("services.upload_manager.server_conection.ssh_connection", side_effect=Exception("fail")):
        result = server_conection.delete_remote_directory_if_empty("/remote/dir/file.pdf")
        assert result is False

def test_save_embeddings_success():
    with patch("services.upload_manager.server_conection.ssh_connection") as mock_ssh:
        mock_sftp = MagicMock()
        mock_ssh_inst = MagicMock()
        mock_ssh.return_value = mock_ssh_inst
        mock_ssh_inst.open_sftp.return_value = mock_sftp
        mock_sftp.stat.side_effect = IOError()
        mock_sftp.mkdir = MagicMock()
        mock_sftp.open.return_value.__enter__.return_value.write = MagicMock()
        index_buffer = io.BytesIO(b"index")
        meta_buffer = io.BytesIO(b"meta")
        result = server_conection.save_embeddings("/remote/path", index_buffer, meta_buffer)
        assert isinstance(result, tuple)

def test_save_embeddings_error():
    with patch("services.upload_manager.server_conection.ssh_connection", side_effect=Exception("fail")):
        index_buffer = io.BytesIO(b"index")
        meta_buffer = io.BytesIO(b"meta")
        result = server_conection.save_embeddings("/remote/path", index_buffer, meta_buffer)
        assert result is None
