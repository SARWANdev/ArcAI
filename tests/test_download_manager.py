import pytest
from unittest.mock import patch, MagicMock
from services.download_manager import download_manager
import io
import zipfile

def test_get_project_note():
    with patch('services.download_manager.download_manager.ProjectDataBase.get_note', return_value='project note'):
        note = download_manager.get_project_note('proj1')
        assert note == b'project note'

def test_get_document_note():
    with patch('services.download_manager.download_manager.DocumentRepository.get_note', return_value='doc note'):
        note = download_manager.get_document_note('doc1')
        assert note == b'doc note'

def test_get_document_bibtex():
    with patch('services.download_manager.download_manager.DocumentRepository.get_pdf_master_id', return_value='pdf1'), \
         patch('services.download_manager.download_manager.PdfMasterRepository.get_bibtex', return_value='@bibtex'):
        bib = download_manager.get_document_bibtex('doc1')
        assert bib == b'@bibtex'

def test_download_file():
    with patch('services.download_manager.download_manager.DocumentRepository.get_pdf_master_id', return_value='pdf1'), \
         patch('services.download_manager.download_manager.PdfMasterRepository.get_pdf_hash', return_value='hash'), \
         patch('services.download_manager.download_manager.format_filename', return_value='DocName'), \
         patch('services.download_manager.download_manager.DocumentRepository.get_name', return_value='DocName'), \
         patch('services.download_manager.download_manager.DocumentRepository.get_path', return_value='/remote/path'), \
         patch('services.download_manager.download_manager.get_document_note', return_value=b'note'), \
         patch('services.download_manager.download_manager.get_document_bibtex', return_value=b'bib'), \
         patch('services.download_manager.download_manager.ssh_connection') as mock_ssh:
        mock_sftp = MagicMock()
        mock_ssh_inst = MagicMock()
        mock_ssh.return_value = mock_ssh_inst
        mock_ssh_inst.open_sftp.return_value = mock_sftp
        mock_sftp.open.return_value.__enter__.return_value.read.return_value = b'pdfdata'
        zip_bytes = download_manager.download_file('doc1')
        with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zipf:
            assert 'note.txt' in zipf.namelist()
            assert 'bibtex.bib' in zipf.namelist()
            assert 'DocName.pdf' in zipf.namelist()

def test_download_multiple_bibtex():
    with patch('services.download_manager.download_manager.ssh_connection') as mock_ssh, \
         patch('services.download_manager.download_manager.DocumentRepository.get_name', return_value='DocName'), \
         patch('services.download_manager.download_manager.get_document_bibtex', return_value=b'bib'):
        mock_sftp = MagicMock()
        mock_ssh_inst = MagicMock()
        mock_ssh.return_value = mock_ssh_inst
        mock_ssh_inst.open_sftp.return_value = mock_sftp
        zip_bytes = download_manager.download_multiple_bibtex(['doc1'])
        with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zipf:
            assert 'DocName_bibtex.bib' in zipf.namelist()

def test_download_multiple_documents():
    with patch('services.download_manager.download_manager.ssh_connection') as mock_ssh, \
         patch('services.download_manager.download_manager.get_project_note', return_value=b'project note'), \
         patch('services.download_manager.download_manager.DocumentRepository.get_pdf_master_id', return_value='pdf1'), \
         patch('services.download_manager.download_manager.PdfMasterRepository.get_pdf_hash', return_value='hash'), \
         patch('services.download_manager.download_manager.format_filename', return_value='DocName'), \
         patch('services.download_manager.download_manager.DocumentRepository.get_name', return_value='DocName'), \
         patch('services.download_manager.download_manager.DocumentRepository.get_path', return_value='/remote/path'), \
         patch('services.download_manager.download_manager.get_document_note', return_value=b'note'), \
         patch('services.download_manager.download_manager.get_document_bibtex', return_value=b'bib'):
        mock_sftp = MagicMock()
        mock_ssh_inst = MagicMock()
        mock_ssh.return_value = mock_ssh_inst
        mock_ssh_inst.open_sftp.return_value = mock_sftp
        mock_sftp.open.return_value.__enter__.return_value.read.return_value = b'pdfdata'
        zip_bytes = download_manager.download_multiple_documents(['doc1'], 'proj1')
        with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zipf:
            assert 'project_note.txt' in zipf.namelist()
            assert 'DocName/note.txt' in zipf.namelist()
            assert 'DocName/bibtex.bib' in zipf.namelist()
            assert 'DocName/DocName.pdf' in zipf.namelist()

def test_download_project():
    with patch('services.download_manager.download_manager.DocumentService.get_document_ids_from_project_id', return_value=['doc1']), \
         patch('services.download_manager.download_manager.download_multiple_documents', return_value=b'zipbytes'):
        result = download_manager.download_project('proj1')
        assert result == b'zipbytes'

def test_download_project_bibtex():
    with patch('services.download_manager.download_manager.DocumentService.get_document_ids_from_project_id', return_value=['doc1']), \
         patch('services.download_manager.download_manager.download_multiple_bibtex', return_value=b'zipbytes'):
        result = download_manager.download_project_bibtex('proj1')
        assert result == b'zipbytes'
