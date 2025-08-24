import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from database.repository.document_properties_repository import DocumentPropertiesRepository
from exceptions.tag_exceptions import InvalidTagName, MissingTagColor

FAKE_DOCUMENT_ID = "64b2fae99a8b5c5f12345678"
FAKE_PROJECT_ID = "64b2fae99a8b5c5f87654321"
FAKE_PDF_MASTER_ID = "64b2fae99a8b5c5f11111111"


@pytest.fixture
def mock_db():
    """Returns a fake DB connection mock."""
    mock_db = MagicMock()
    mock_db.documents = MagicMock()
    return mock_db


class TestMarkAsFavorite:
    """Test cases for mark_as_favorite method."""

    def test_mark_as_favorite_success(self, mock_db):
        """Test successful marking of document as favorite."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = DocumentPropertiesRepository.mark_as_favorite(FAKE_DOCUMENT_ID)
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"favorite": True}}
            )

    def test_mark_as_favorite_no_modification(self, mock_db):
        """Test marking as favorite when document doesn't exist."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 0

            result = DocumentPropertiesRepository.mark_as_favorite(FAKE_DOCUMENT_ID)
            
            assert result is False

    def test_mark_as_favorite_exception(self, mock_db):
        """Test handling of database exceptions during mark as favorite."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.side_effect = Exception("Database error")

            result = DocumentPropertiesRepository.mark_as_favorite(FAKE_DOCUMENT_ID)
            
            assert result is False


class TestMarkAsNotFavorite:
    """Test cases for mark_as_not_favorite method."""

    def test_mark_as_not_favorite_success(self, mock_db):
        """Test successful marking of document as not favorite."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = DocumentPropertiesRepository.mark_as_not_favorite(FAKE_DOCUMENT_ID)
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"favorite": False}}
            )

    def test_mark_as_not_favorite_no_modification(self, mock_db):
        """Test marking as not favorite when document doesn't exist."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 0

            result = DocumentPropertiesRepository.mark_as_not_favorite(FAKE_DOCUMENT_ID)
            
            assert result is False

    def test_mark_as_not_favorite_exception(self, mock_db):
        """Test handling of database exceptions during mark as not favorite."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.side_effect = Exception("Database error")

            result = DocumentPropertiesRepository.mark_as_not_favorite(FAKE_DOCUMENT_ID)
            
            assert result is False


class TestMarkAsRead:
    """Test cases for mark_as_read method."""

    def test_mark_as_read_success(self, mock_db):
        """Test successful marking of document as read."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = DocumentPropertiesRepository.mark_as_read(FAKE_DOCUMENT_ID)
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"read": True}}
            )

    def test_mark_as_read_no_modification(self, mock_db):
        """Test marking as read when document doesn't exist."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 0

            result = DocumentPropertiesRepository.mark_as_read(FAKE_DOCUMENT_ID)
            
            assert result is False

    def test_mark_as_read_exception(self, mock_db):
        """Test handling of database exceptions during mark as read."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.side_effect = Exception("Database error")

            result = DocumentPropertiesRepository.mark_as_read(FAKE_DOCUMENT_ID)
            
            assert result is False


class TestMarkAsNotRead:
    """Test cases for mark_as_not_read method."""

    def test_mark_as_not_read_success(self, mock_db):
        """Test successful marking of document as not read."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = DocumentPropertiesRepository.mark_as_not_read(FAKE_DOCUMENT_ID)
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"read": False}}
            )

    def test_mark_as_not_read_no_modification(self, mock_db):
        """Test marking as not read when document doesn't exist."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 0

            result = DocumentPropertiesRepository.mark_as_not_read(FAKE_DOCUMENT_ID)
            
            assert result is False

    def test_mark_as_not_read_exception(self, mock_db):
        """Test handling of database exceptions during mark as not read."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.side_effect = Exception("Database error")

            result = DocumentPropertiesRepository.mark_as_not_read(FAKE_DOCUMENT_ID)
            
            assert result is False


class TestUpdateJournal:
    """Test cases for update_journal method."""

    def test_update_journal_success(self, mock_db):
        """Test successful journal update."""
        journal_name = "Nature"
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = DocumentPropertiesRepository.update_journal(FAKE_DOCUMENT_ID, journal_name)
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"journal": journal_name}}
            )

    def test_update_journal_no_modification(self, mock_db):
        """Test journal update when document doesn't exist."""
        journal_name = "Science"
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 0

            result = DocumentPropertiesRepository.update_journal(FAKE_DOCUMENT_ID, journal_name)
            
            assert result is False

    def test_update_journal_exception(self, mock_db):
        """Test handling of database exceptions during journal update."""
        journal_name = "Cell"
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.side_effect = Exception("Database error")

            result = DocumentPropertiesRepository.update_journal(FAKE_DOCUMENT_ID, journal_name)
            
            assert result is False


class TestUpdateTag:
    """Test cases for update_tag method."""

    def test_update_tag_success(self, mock_db):
        """Test successful tag update."""
        tag_name = "research"
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = DocumentPropertiesRepository.update_tag(FAKE_DOCUMENT_ID, tag_name)
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"tag_name": tag_name}}
            )

    def test_update_tag_none_value(self, mock_db):
        """Test tag update with None value (removing tag)."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = DocumentPropertiesRepository.update_tag(FAKE_DOCUMENT_ID, None)
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"tag_name": None}}
            )

    def test_update_tag_empty_string(self, mock_db):
        """Test tag update with empty string."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = DocumentPropertiesRepository.update_tag(FAKE_DOCUMENT_ID, "")
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"tag_name": ""}}
            )

    def test_update_tag_whitespace_trimming(self, mock_db):
        """Test tag update with whitespace trimming."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = DocumentPropertiesRepository.update_tag(FAKE_DOCUMENT_ID, "  research  ")
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"tag_name": "research"}}
            )

    def test_update_tag_invalid_type(self):
        """Test tag update with invalid type."""
        with pytest.raises(InvalidTagName, match="Tag name must be a string"):
            DocumentPropertiesRepository.update_tag(FAKE_DOCUMENT_ID, 123)

    def test_update_tag_too_short(self):
        """Test tag update with too short name."""
        with pytest.raises(InvalidTagName, match="Tag name must be at least 1 character long"):
            DocumentPropertiesRepository.update_tag(FAKE_DOCUMENT_ID, "")

    def test_update_tag_too_long(self):
        """Test tag update with too long name."""
        long_tag = "a" * 41  # Exceeds MAX_NAME_LENGTH of 40
        with pytest.raises(InvalidTagName, match="Tag name cannot exceed 40 characters"):
            DocumentPropertiesRepository.update_tag(FAKE_DOCUMENT_ID, long_tag)

    def test_update_tag_exception(self, mock_db):
        """Test handling of database exceptions during tag update."""
        tag_name = "research"
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.side_effect = Exception("Database error")

            result = DocumentPropertiesRepository.update_tag(FAKE_DOCUMENT_ID, tag_name)
            
            assert result is False


class TestUpdateTagColor:
    """Test cases for update_tag_color method."""

    def test_update_tag_color_success(self, mock_db):
        """Test successful tag color update."""
        tag_color = "#FF0000"
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = DocumentPropertiesRepository.update_tag_color(FAKE_DOCUMENT_ID, tag_color)
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"tag_color": tag_color}}
            )

    def test_update_tag_color_none_value(self, mock_db):
        """Test tag color update with None value (removing color)."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = DocumentPropertiesRepository.update_tag_color(FAKE_DOCUMENT_ID, None)
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"tag_color": None}}
            )

    def test_update_tag_color_whitespace_trimming(self, mock_db):
        """Test tag color update with whitespace trimming."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = DocumentPropertiesRepository.update_tag_color(FAKE_DOCUMENT_ID, "  #FF0000  ")
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"tag_color": "#FF0000"}}
            )

    def test_update_tag_color_invalid_type(self):
        """Test tag color update with invalid type."""
        with pytest.raises(MissingTagColor, match="Tag color must be a string"):
            DocumentPropertiesRepository.update_tag_color(FAKE_DOCUMENT_ID, 123)

    def test_update_tag_color_empty_after_trim(self):
        """Test tag color update with empty string after trimming."""
        with pytest.raises(MissingTagColor, match="Tag color cannot be empty"):
            DocumentPropertiesRepository.update_tag_color(FAKE_DOCUMENT_ID, "   ")

    def test_update_tag_color_exception(self, mock_db):
        """Test handling of database exceptions during tag color update."""
        tag_color = "#FF0000"
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.side_effect = Exception("Database error")

            result = DocumentPropertiesRepository.update_tag_color(FAKE_DOCUMENT_ID, tag_color)
            
            assert result is False


class TestSetNewProjectId:
    """Test cases for set_new_project_id method."""

    def test_set_new_project_id_success(self, mock_db):
        """Test successful project ID update."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = DocumentPropertiesRepository.set_new_project_id(FAKE_DOCUMENT_ID, FAKE_PROJECT_ID)
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"project_id": FAKE_PROJECT_ID}}
            )

    def test_set_new_project_id_no_modification(self, mock_db):
        """Test project ID update when document doesn't exist."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 0

            result = DocumentPropertiesRepository.set_new_project_id(FAKE_DOCUMENT_ID, FAKE_PROJECT_ID)
            
            assert result is False

    def test_set_new_project_id_exception(self, mock_db):
        """Test handling of database exceptions during project ID update."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.side_effect = Exception("Database error")

            result = DocumentPropertiesRepository.set_new_project_id(FAKE_DOCUMENT_ID, FAKE_PROJECT_ID)
            
            assert result is False


class TestGetProjectId:
    """Test cases for get_project_id method."""

    def test_get_project_id_success(self, mock_db):
        """Test successful project ID retrieval."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.find_one.return_value = {"project_id": FAKE_PROJECT_ID}

            result = DocumentPropertiesRepository.get_project_id(FAKE_DOCUMENT_ID)
            
            assert result == FAKE_PROJECT_ID
            mock_db.documents.find_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"project_id": 1}
            )

    def test_get_project_id_not_found(self, mock_db):
        """Test project ID retrieval when document doesn't exist."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.find_one.return_value = None

            result = DocumentPropertiesRepository.get_project_id(FAKE_DOCUMENT_ID)
            
            assert result is None

    def test_get_project_id_no_project_id_field(self, mock_db):
        """Test project ID retrieval when document has no project_id field."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.find_one.return_value = {"_id": ObjectId(FAKE_DOCUMENT_ID)}

            result = DocumentPropertiesRepository.get_project_id(FAKE_DOCUMENT_ID)
            
            assert result is None

    def test_get_project_id_exception(self, mock_db):
        """Test handling of database exceptions during project ID retrieval."""
        with patch("database.repository.document_properties_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.find_one.side_effect = Exception("Database error")

            result = DocumentPropertiesRepository.get_project_id(FAKE_DOCUMENT_ID)
            
            assert result == ""


class TestGetFirstAuthor:
    """Test cases for get_first_author method."""

    def test_get_first_author_success(self, mock_db):
        """Test successful first author retrieval."""
        with patch("database.repository.document_properties_repository.DocumentRepository.get_pdf_master_id") as mock_get_pdf_id, \
             patch("database.repository.document_properties_repository.PdfMasterRepository.get_first_author") as mock_get_author:
            mock_get_pdf_id.return_value = FAKE_PDF_MASTER_ID
            mock_get_author.return_value = "John Doe"

            result = DocumentPropertiesRepository.get_first_author(FAKE_DOCUMENT_ID)
            
            assert result == "John Doe"
            mock_get_pdf_id.assert_called_once_with(FAKE_DOCUMENT_ID)
            mock_get_author.assert_called_once_with(FAKE_PDF_MASTER_ID)

    def test_get_first_author_no_pdf_master_id(self, mock_db):
        """Test first author retrieval when no PDF master ID exists."""
        with patch("database.repository.document_properties_repository.DocumentRepository.get_pdf_master_id") as mock_get_pdf_id, \
             patch("database.repository.document_properties_repository.PdfMasterRepository.get_first_author") as mock_get_author:
            mock_get_pdf_id.return_value = None
            mock_get_author.return_value = "Unknown"

            result = DocumentPropertiesRepository.get_first_author(FAKE_DOCUMENT_ID)
            
            assert result == "Unknown"
            mock_get_pdf_id.assert_called_once_with(FAKE_DOCUMENT_ID)
            mock_get_author.assert_called_once_with(None)


class TestGetProjectIdAndName:
    """Test cases for get_project_id_and_name method."""

    def test_get_project_id_and_name_success(self, mock_db):
        """Test successful project ID and name retrieval."""
        with patch("database.repository.document_properties_repository.DocumentPropertiesRepository.get_project_id") as mock_get_id, \
             patch("database.repository.document_properties_repository.Project.get_project_name") as mock_get_name:
            mock_get_id.return_value = FAKE_PROJECT_ID
            mock_get_name.return_value = "Research Project"

            result = DocumentPropertiesRepository.get_project_id_and_name(FAKE_DOCUMENT_ID)
            
            assert result == (FAKE_PROJECT_ID, "Research Project")
            mock_get_id.assert_called_once_with(FAKE_DOCUMENT_ID)
            mock_get_name.assert_called_once_with(FAKE_PROJECT_ID)

    def test_get_project_id_and_name_no_project_id(self, mock_db):
        """Test project ID and name retrieval when no project ID exists."""
        with patch("database.repository.document_properties_repository.DocumentPropertiesRepository.get_project_id") as mock_get_id, \
             patch("database.repository.document_properties_repository.Project.get_project_name") as mock_get_name:
            mock_get_id.return_value = ""
            # get_project_name should not be called when project_id is empty
            mock_get_name.return_value = "Research Project"

            result = DocumentPropertiesRepository.get_project_id_and_name(FAKE_DOCUMENT_ID)
            
            assert result == ("", "")
            mock_get_id.assert_called_once_with(FAKE_DOCUMENT_ID)
            mock_get_name.assert_not_called()

    def test_get_project_id_and_name_none_project_id(self, mock_db):
        """Test project ID and name retrieval when project ID is None."""
        with patch("database.repository.document_properties_repository.DocumentPropertiesRepository.get_project_id") as mock_get_id, \
             patch("database.repository.document_properties_repository.Project.get_project_name") as mock_get_name:
            mock_get_id.return_value = None
            # get_project_name should not be called when project_id is None
            mock_get_name.return_value = "Research Project"

            result = DocumentPropertiesRepository.get_project_id_and_name(FAKE_DOCUMENT_ID)
            
            assert result == ("", "")
            mock_get_id.assert_called_once_with(FAKE_DOCUMENT_ID)
            mock_get_name.assert_not_called()
