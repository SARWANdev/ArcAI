import pytest
from unittest.mock import patch, MagicMock
from services.document_service import DocumentService

@pytest.fixture
def document_service():
    return DocumentService()

@pytest.fixture
def fake_document_data():
    return {
        'name': 'Test Doc',
        'project_id': 'proj1',
        'pdf_master_id': 'pdf1',
        'note': 'note',
        'tag_name': 'tag',
        'tag_color': 'blue',
        'read': True,
        'favorite': False,
        'created_at': '2025-08-23T00:00:00Z',
        'updated_at': '2025-08-23T00:00:00Z'
    }


def test_get_document_not_found(document_service):
    with patch.object(document_service.document_repository, 'get_by_document_id', return_value=None):
        doc = document_service.get_document('docid')
        assert doc is None

def test_add_tag_success(document_service):
    with patch('services.document_service.TagRegistryRepository.get_tag', return_value=None), \
         patch('services.document_service.TagRegistryRepository.create_or_verify_tag'), \
         patch.object(document_service.document_properties_repo, 'update_tag', return_value=True), \
         patch.object(document_service.document_properties_repo, 'update_tag_color', return_value=True):
        result = document_service.add_tag('docid', 'tag', 'blue')
        assert result is True

def test_add_tag_color_match(document_service):
    with patch('services.document_service.TagRegistryRepository.get_tag', return_value={"color": "blue"}), \
         patch.object(document_service.document_properties_repo, 'update_tag', return_value=True), \
         patch.object(document_service.document_properties_repo, 'update_tag_color', return_value=True):
        result = document_service.add_tag('docid', 'tag', 'blue')
        assert result is True

def test_add_tag_existing_color_mismatch(document_service):
    with patch('services.document_service.TagRegistryRepository.get_tag', return_value={"color": "red"}), \
         patch.object(document_service.document_properties_repo, 'update_tag'), \
         patch.object(document_service.document_properties_repo, 'update_tag_color'):
        result = document_service.add_tag('docid', 'tag', 'blue')
        assert result is False

def test_add_tag_update_tag_fail(document_service):
    with patch('services.document_service.TagRegistryRepository.get_tag', return_value=None), \
         patch('services.document_service.TagRegistryRepository.create_or_verify_tag'), \
         patch.object(document_service.document_properties_repo, 'update_tag', return_value=False), \
         patch.object(document_service.document_properties_repo, 'update_tag_color', return_value=True):
        result = document_service.add_tag('docid', 'tag', 'blue')
        assert result is False

def test_add_tag_update_tag_color_fail(document_service):
    with patch('services.document_service.TagRegistryRepository.get_tag', return_value=None), \
         patch('services.document_service.TagRegistryRepository.create_or_verify_tag'), \
         patch.object(document_service.document_properties_repo, 'update_tag', return_value=True), \
         patch.object(document_service.document_properties_repo, 'update_tag_color', return_value=False):
        result = document_service.add_tag('docid', 'tag', 'blue')
        assert result is False

def test_add_tag_exception(document_service):
    with patch('services.document_service.TagRegistryRepository.get_tag', side_effect=Exception('fail')):
        result = document_service.add_tag('docid', 'tag', 'blue')
        assert result is False

def test_delete_document_success(document_service):
    with patch.object(document_service.document_repository, 'get_pdf_master_id', return_value='pdf1'), \
         patch.object(document_service.document_repository, 'delete_document', return_value={'_id': 'docid'}), \
         patch.object(document_service.pdf_master_repository, 'get_path', return_value='/tmp/path'), \
         patch.object(document_service.pdf_master_repository, 'decrement_ref_count'), \
         patch.object(document_service.conversation_repository, 'delete_conversation_for_document'), \
         patch.object(document_service.pdf_master_repository, 'get_ref_count', return_value=0), \
         patch('services.document_service.delete_remote_directory'), \
         patch.object(document_service.pdf_master_repository, 'delete_pdf_master'):
        assert document_service.delete_document('docid') is True

def test_delete_document_not_found(document_service):
    with patch.object(document_service.document_repository, 'get_pdf_master_id', return_value='pdf1'), \
         patch.object(document_service.document_repository, 'delete_document', return_value=None):
        assert document_service.delete_document('docid') is False

def test_delete_document_exception(document_service):
    with patch.object(document_service.document_repository, 'get_pdf_master_id', side_effect=Exception('fail')):
        assert document_service.delete_document('docid') is False

def test_mark_as_read(document_service):
    with patch.object(document_service.document_properties_repo, 'mark_as_read', return_value=True):
        assert document_service.mark_as_read('docid') is True

def test_mark_as_unread(document_service):
    with patch.object(document_service.document_properties_repo, 'mark_as_not_read', return_value=True):
        assert document_service.mark_as_unread('docid') is True

def test_add_to_favorites(document_service):
    with patch.object(document_service.document_properties_repo, 'mark_as_favorite', return_value=True):
        assert document_service.add_to_favorites('docid') is True

def test_remove_from_favorites(document_service):
    with patch.object(document_service.document_properties_repo, 'mark_as_not_favorite', return_value=True):
        assert document_service.remove_from_favorites('docid') is True

def test_remove_tag_success(document_service, fake_document_data):
    with patch.object(document_service.document_repository, 'get_by_document_id', return_value=fake_document_data), \
         patch.object(document_service.document_properties_repo, 'update_tag', return_value=True), \
         patch.object(document_service.document_properties_repo, 'update_tag_color', return_value=True), \
         patch('services.document_service.mongo_connection'), \
         patch('services.document_service.TagRegistryRepository.get_tag', return_value=None):
        assert document_service.remove_tag('docid') is True

def test_remove_tag_update_tag_fail(document_service, fake_document_data):
    with patch.object(document_service.document_repository, 'get_by_document_id', return_value=fake_document_data), \
         patch.object(document_service.document_properties_repo, 'update_tag', return_value=False), \
         patch.object(document_service.document_properties_repo, 'update_tag_color', return_value=True), \
         patch('services.document_service.mongo_connection'), \
         patch('services.document_service.TagRegistryRepository.get_tag', return_value=None):
        assert document_service.remove_tag('docid') is False

def test_remove_tag_update_tag_color_fail(document_service, fake_document_data):
    with patch.object(document_service.document_repository, 'get_by_document_id', return_value=fake_document_data), \
         patch.object(document_service.document_properties_repo, 'update_tag', return_value=True), \
         patch.object(document_service.document_properties_repo, 'update_tag_color', return_value=False), \
         patch('services.document_service.mongo_connection'), \
         patch('services.document_service.TagRegistryRepository.get_tag', return_value=None):
        assert document_service.remove_tag('docid') is False

def test_remove_tag_exception(document_service, fake_document_data):
    with patch.object(document_service.document_repository, 'get_by_document_id', side_effect=Exception('fail')):
        assert document_service.remove_tag('docid') is False

def test_get_document_tag(document_service, fake_document_data):
    with patch.object(document_service.document_repository, 'get_by_document_id', return_value=fake_document_data):
        tag = document_service.get_document_tag('docid')
        assert tag is not None
        assert tag.tag_name == 'tag'
        assert tag.tag_color == 'blue'

def test_get_document_tag_none(document_service):
    with patch.object(document_service.document_repository, 'get_by_document_id', return_value=None):
        tag = document_service.get_document_tag('docid')
        assert tag is None

def test_get_document_tag_exception(document_service):
    with patch.object(document_service.document_repository, 'get_by_document_id', side_effect=Exception('fail')):
        tag = document_service.get_document_tag('docid')
        assert tag is None

def test_get_project_tags(document_service, fake_document_data):
    with patch.object(document_service, 'get_project_documents', return_value=[MagicMock(get_tag_name=MagicMock(return_value='tag'))]), \
         patch('services.document_service.TagRegistryRepository.get_tag', return_value={'color': 'blue'}):
        tags = document_service.get_project_tags('proj1')
        assert tags == {'tag': 'blue'}

def test_get_project_tags_tag_none(document_service):
    with patch.object(document_service, 'get_project_documents', return_value=[MagicMock(get_tag_name=MagicMock(return_value='tag'))]), \
         patch('services.document_service.TagRegistryRepository.get_tag', return_value=None):
        tags = document_service.get_project_tags('proj1')
        assert tags == {'tag': None}

def test_get_project_tags_multiple(document_service):
    doc1 = MagicMock(get_tag_name=MagicMock(return_value='tag1'))
    doc2 = MagicMock(get_tag_name=MagicMock(return_value='tag2'))
    with patch.object(document_service, 'get_project_documents', return_value=[doc1, doc2]), \
         patch('services.document_service.TagRegistryRepository.get_tag', side_effect=[{'color': 'blue'}, {'color': 'red'}]):
        tags = document_service.get_project_tags('proj1')
        assert tags == {'tag1': 'blue', 'tag2': 'red'}

def test_get_project_tags_empty(document_service):
    with patch.object(document_service, 'get_project_documents', return_value=None):
        tags = document_service.get_project_tags('proj1')
        assert tags == {}

def test_get_project_tags_exception(document_service):
    with patch.object(document_service, 'get_project_documents', side_effect=Exception('fail')):
        tags = document_service.get_project_tags('proj1')
        assert tags == {}

def test_get_document_ids_from_project_id(document_service):
    with patch.object(document_service, 'get_project_documents', return_value=[MagicMock(document_id='doc1'), MagicMock(document_id='doc2')]):
        ids = document_service.get_document_ids_from_project_id('proj1')
        assert ids == ['doc1', 'doc2']

def test_get_document_ids_from_project_id_empty(document_service):
    with patch.object(document_service, 'get_project_documents', return_value=[]):
        ids = document_service.get_document_ids_from_project_id('proj1')
        assert ids == []

def test_get_document_ids_from_project_id_exception(document_service):
    with patch.object(type(document_service), 'get_project_documents', side_effect=Exception('fail')):
        ids = document_service.get_document_ids_from_project_id('proj1')
        assert ids == []

def test_filter_documents(document_service):
    doc1 = MagicMock(is_read=MagicMock(return_value=True), is_favorite=MagicMock(return_value=True), get_tag_name=MagicMock(return_value='tag1'))
    doc2 = MagicMock(is_read=MagicMock(return_value=False), is_favorite=MagicMock(return_value=False), get_tag_name=MagicMock(return_value='tag2'))
    with patch.object(document_service, 'get_project_documents', return_value=[doc1, doc2]):
        filtered = document_service.filter_documents('proj1', read=True)
        assert filtered == [doc1]
        filtered = document_service.filter_documents('proj1', favorite=False)
        assert filtered == [doc2]
        filtered = document_service.filter_documents('proj1', tag='tag1')
        assert filtered == [doc1]

def test_filter_documents_none(document_service):
    with patch.object(document_service, 'get_project_documents', return_value=None):
        filtered = document_service.filter_documents('proj1', read=True)
        assert filtered == []

def test_filter_documents_exception(document_service):
    with patch.object(document_service, 'get_project_documents', side_effect=Exception('fail')):
        filtered = document_service.filter_documents('proj1', read=True)
        assert filtered == []

def test_get_filtered_and_sorted_documents(document_service):
    doc1 = MagicMock()
    doc1.name = 'B'
    doc1.created_at = '2025-08-23T00:00:00Z'
    doc1.document_id = 'doc1'

    doc2 = MagicMock()
    doc2.name = 'A'
    doc2.created_at = '2025-08-22T00:00:00Z'
    doc2.document_id = 'doc2'

    with patch.object(document_service, 'filter_documents', return_value=[doc1, doc2]), \
         patch.object(document_service.document_repository, 'get_authors', return_value='author'), \
         patch.object(document_service.document_repository, 'get_year', return_value='2025'), \
         patch.object(document_service.document_repository, 'get_source', return_value='source'):
        sorted_docs = document_service.get_filtered_and_sorted_documents('proj1', 'title', 'asc')
        assert sorted_docs[0].name == 'A'
        sorted_docs = document_service.get_filtered_and_sorted_documents('proj1', 'created_at', 'desc')
        assert sorted_docs[0].created_at == '2025-08-23T00:00:00Z'

def test_get_filtered_and_sorted_documents_empty(document_service):
    with patch.object(document_service, 'filter_documents', return_value=[]):
        sorted_docs = document_service.get_filtered_and_sorted_documents('proj1', 'title', 'asc')
        assert sorted_docs == []

def test_get_filtered_and_sorted_documents_invalid_sort(document_service):
    doc1 = MagicMock(name='B', created_at='2025-08-23T00:00:00Z', document_id='doc1')
    with patch.object(document_service, 'filter_documents', return_value=[doc1]), \
         patch.object(document_service.document_repository, 'get_authors', return_value='author'), \
         patch.object(document_service.document_repository, 'get_year', return_value='2025'), \
         patch.object(document_service.document_repository, 'get_source', return_value='source'):
        sorted_docs = document_service.get_filtered_and_sorted_documents('proj1', 'invalid', 'asc')
        assert sorted_docs[0] == doc1

def test_get_filtered_and_sorted_documents_exception(document_service):
    with patch.object(document_service, 'filter_documents', side_effect=Exception('fail')):
        sorted_docs = document_service.get_filtered_and_sorted_documents('proj1', 'title', 'asc')
        assert sorted_docs == []

def test_rename_document(document_service):
    with patch.object(document_service.document_repository, 'update_document_name', return_value=True):
        assert document_service.rename_document('docid', 'newname') is True
    with patch.object(document_service.document_repository, 'update_document_name', return_value=False):
        assert document_service.rename_document('docid', 'newname') is False

def test_rename_document_exception(document_service):
    with patch.object(document_service.document_repository, 'update_document_name', side_effect=Exception('fail')):
        assert document_service.rename_document('docid', 'newname') is False

def test_duplicate_document(document_service):
    with patch.object(document_service.document_repository, 'get_pdf_master_id', return_value='pdf1'), \
         patch.object(document_service.document_repository, 'get_name', return_value='docname'), \
         patch.object(document_service, '_DocumentService__create_document') as mock_create:
        document_service.duplicate_document('docid', 'projid')
        mock_create.assert_called_once()

def test_duplicate_document_exception(document_service):
    with patch.object(document_service.document_repository, 'get_pdf_master_id', side_effect=Exception('fail')):
        result = document_service.duplicate_document('docid', 'projid')
        assert result is None

def test_move_document(document_service):
    with patch.object(document_service.document_properties_repo, 'set_new_project_id') as mock_set:
        document_service.move_document('docid', 'projid')
        mock_set.assert_called_once_with('docid', 'projid')

def test_move_document_exception(document_service):
    with patch.object(document_service.document_properties_repo, 'set_new_project_id', side_effect=Exception('fail')):
        result = document_service.move_document('docid', 'projid')
        assert result is None

def test_search_documents(document_service):
    with patch.object(document_service.document_repository, 'search_documents', return_value=[{'id': 'doc1'}]), \
         patch.object(document_service.document_repository, 'get_by_document_id', return_value={'document_id': 'doc1'}), \
         patch('model.document_reader.document.Document.from_dict', return_value=MagicMock()):
        docs = document_service.search_documents('user1', 'query')
        assert isinstance(docs, list)
    with patch.object(document_service.document_repository, 'search_documents', return_value=None), \
         patch.object(document_service.document_repository, 'search_contents', return_value=None):
        docs = document_service.search_documents('user1', 'query')
        assert docs == []

def test_search_documents_exception(document_service):
    with patch.object(document_service.document_repository, 'search_documents', side_effect=Exception('fail')):
        docs = document_service.search_documents('user1', 'query')
        assert docs == []


