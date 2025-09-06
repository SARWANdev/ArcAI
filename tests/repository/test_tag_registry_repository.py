import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from database.repository.tag_registry_repository import TagRegistryRepository
from exceptions.tag_exceptions import DuplicateTagColor, MissingTagColor
from exceptions.base_exceptions import InvalidNameError

FAKE_TAG_ID = "64b2fae99a8b5c5f12345678"
FAKE_TAG_NAME = "research"
FAKE_TAG_COLOR = "#FF0000"


@pytest.fixture
def mock_db():
    """Returns a fake DB connection mock."""
    mock_db = MagicMock()
    mock_db.tag_registry = MagicMock()
    return mock_db


class TestEnsureIndexes:
    """Test cases for ensure_indexes method."""

    def test_ensure_indexes_success(self, mock_db):
        """Test successful creation of indexes."""
        with patch("database.repository.tag_registry_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.tag_registry.create_index.return_value = "index_created"

            result = TagRegistryRepository.ensure_indexes()
            
            assert result is None
            mock_db.tag_registry.create_index.assert_called_once_with([("name", 1)], unique=True)

    def test_ensure_indexes_exception(self, mock_db):
        """Test handling of database exceptions during index creation."""
        with patch("database.repository.tag_registry_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.tag_registry.create_index.side_effect = Exception("Database error")

            with pytest.raises(Exception, match="Database error"):
                TagRegistryRepository.ensure_indexes()


class TestGetTag:
    """Test cases for get_tag method."""

    def test_get_tag_success(self, mock_db):
        """Test successful tag retrieval."""
        fake_tag = {
            "_id": ObjectId(FAKE_TAG_ID),
            "name": FAKE_TAG_NAME,
            "color": FAKE_TAG_COLOR
        }
        with patch("database.repository.tag_registry_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.tag_registry.find_one.return_value = fake_tag

            result = TagRegistryRepository.get_tag(FAKE_TAG_NAME)
            
            assert result == fake_tag
            mock_db.tag_registry.find_one.assert_called_once_with({"name": FAKE_TAG_NAME})

    def test_get_tag_not_found(self, mock_db):
        """Test tag retrieval when tag doesn't exist."""
        with patch("database.repository.tag_registry_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.tag_registry.find_one.return_value = None

            result = TagRegistryRepository.get_tag(FAKE_TAG_NAME)
            
            assert result is None
            mock_db.tag_registry.find_one.assert_called_once_with({"name": FAKE_TAG_NAME})

    def test_get_tag_empty_string(self, mock_db):
        """Test tag retrieval with empty string."""
        with patch("database.repository.tag_registry_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.tag_registry.find_one.return_value = None

            result = TagRegistryRepository.get_tag("")
            
            assert result is None
            mock_db.tag_registry.find_one.assert_called_once_with({"name": ""})

    def test_get_tag_exception(self, mock_db):
        """Test handling of database exceptions during tag retrieval."""
        with patch("database.repository.tag_registry_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.tag_registry.find_one.side_effect = Exception("Database error")

            with pytest.raises(Exception, match="Database error"):
                TagRegistryRepository.get_tag(FAKE_TAG_NAME)


class TestCreateOrVerifyTag:
    """Test cases for create_or_verify_tag method."""

    def test_create_or_verify_tag_success_new_tag(self, mock_db):
        """Test successful creation of a new tag."""
        with patch("database.repository.tag_registry_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.tag_registry.find_one.return_value = None
            mock_db.tag_registry.insert_one.return_value.inserted_id = ObjectId(FAKE_TAG_ID)

            result = TagRegistryRepository.create_or_verify_tag(FAKE_TAG_NAME, FAKE_TAG_COLOR)
            
            expected_tag = {
                "_id": ObjectId(FAKE_TAG_ID),
                "name": FAKE_TAG_NAME,
                "color": FAKE_TAG_COLOR
            }
            assert result == expected_tag
            mock_db.tag_registry.find_one.assert_called_once_with({"name": FAKE_TAG_NAME})
            mock_db.tag_registry.insert_one.assert_called_once_with({
                "name": FAKE_TAG_NAME,
                "color": FAKE_TAG_COLOR
            })

    def test_create_or_verify_tag_existing_same_color(self, mock_db):
        """Test verification of existing tag with same color."""
        existing_tag = {
            "_id": ObjectId(FAKE_TAG_ID),
            "name": FAKE_TAG_NAME,
            "color": FAKE_TAG_COLOR
        }
        with patch("database.repository.tag_registry_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.tag_registry.find_one.return_value = existing_tag

            result = TagRegistryRepository.create_or_verify_tag(FAKE_TAG_NAME, FAKE_TAG_COLOR)
            
            assert result == existing_tag
            mock_db.tag_registry.find_one.assert_called_once_with({"name": FAKE_TAG_NAME})
            mock_db.tag_registry.insert_one.assert_not_called()

    def test_create_or_verify_tag_existing_different_color(self, mock_db):
        """Test error when existing tag has different color."""
        existing_tag = {
            "_id": ObjectId(FAKE_TAG_ID),
            "name": FAKE_TAG_NAME,
            "color": "#00FF00"  # Different color
        }
        with patch("database.repository.tag_registry_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.tag_registry.find_one.return_value = existing_tag

            with pytest.raises(DuplicateTagColor, match=f"Tag '{FAKE_TAG_NAME}' already exists with different color"):
                TagRegistryRepository.create_or_verify_tag(FAKE_TAG_NAME, FAKE_TAG_COLOR)

    def test_create_or_verify_tag_duplicate_key_error(self, mock_db):
        """Test handling of duplicate key error (race condition)."""
        existing_tag = {
            "_id": ObjectId(FAKE_TAG_ID),
            "name": FAKE_TAG_NAME,
            "color": FAKE_TAG_COLOR
        }
        with patch("database.repository.tag_registry_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.tag_registry.find_one.side_effect = [None, existing_tag]  # First call returns None, second returns existing
            mock_db.tag_registry.insert_one.side_effect = DuplicateKeyError("Duplicate key")

            result = TagRegistryRepository.create_or_verify_tag(FAKE_TAG_NAME, FAKE_TAG_COLOR)
            
            assert result == existing_tag
            assert mock_db.tag_registry.find_one.call_count == 2

    def test_create_or_verify_tag_whitespace_trimming(self, mock_db):
        """Test whitespace trimming of tag name and color."""
        with patch("database.repository.tag_registry_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.tag_registry.find_one.return_value = None
            mock_db.tag_registry.insert_one.return_value.inserted_id = ObjectId(FAKE_TAG_ID)

            result = TagRegistryRepository.create_or_verify_tag("  research  ", "  #FF0000  ")
            
            expected_tag = {
                "_id": ObjectId(FAKE_TAG_ID),
                "name": "research",
                "color": "#FF0000"
            }
            assert result == expected_tag
            mock_db.tag_registry.insert_one.assert_called_once_with({
                "name": "research",
                "color": "#FF0000"
            })

    def test_create_or_verify_tag_invalid_name_none(self):
        """Test validation with None tag name."""
        with pytest.raises(InvalidNameError, match="Tag name must be a non-empty string"):
            TagRegistryRepository.create_or_verify_tag(None, FAKE_TAG_COLOR)

    def test_create_or_verify_tag_invalid_name_empty(self):
        """Test validation with empty tag name."""
        with pytest.raises(InvalidNameError, match="Tag name must be a non-empty string"):
            TagRegistryRepository.create_or_verify_tag("", FAKE_TAG_COLOR)

    def test_create_or_verify_tag_invalid_name_type(self):
        """Test validation with non-string tag name."""
        with pytest.raises(InvalidNameError, match="Tag name must be a non-empty string"):
            TagRegistryRepository.create_or_verify_tag(123, FAKE_TAG_COLOR)

    def test_create_or_verify_tag_name_too_short(self):
        """Test validation with too short tag name."""
        with pytest.raises(InvalidNameError, match="Tag name must be a non-empty string"):
            TagRegistryRepository.create_or_verify_tag("", FAKE_TAG_COLOR)

    def test_create_or_verify_tag_name_too_short_after_trim(self):
        """Test validation with whitespace-only tag name that becomes too short after trimming."""
        with pytest.raises(InvalidNameError, match="Tag name must be at least 1 character long"):
            TagRegistryRepository.create_or_verify_tag(" ", FAKE_TAG_COLOR)

    def test_create_or_verify_tag_name_too_long(self):
        """Test validation with too long tag name."""
        long_name = "a" * 41  # Exceeds MAX_NAME_LENGTH of 40
        with pytest.raises(InvalidNameError, match="Tag name cannot exceed 40 characters"):
            TagRegistryRepository.create_or_verify_tag(long_name, FAKE_TAG_COLOR)

    def test_create_or_verify_tag_invalid_color_none(self):
        """Test validation with None tag color."""
        with pytest.raises(MissingTagColor, match="Tag color must be a non-empty string"):
            TagRegistryRepository.create_or_verify_tag(FAKE_TAG_NAME, None)

    def test_create_or_verify_tag_invalid_color_empty(self):
        """Test validation with empty tag color."""
        with pytest.raises(MissingTagColor, match="Tag color must be a non-empty string"):
            TagRegistryRepository.create_or_verify_tag(FAKE_TAG_NAME, "")

    def test_create_or_verify_tag_invalid_color_type(self):
        """Test validation with non-string tag color."""
        with pytest.raises(MissingTagColor, match="Tag color must be a non-empty string"):
            TagRegistryRepository.create_or_verify_tag(FAKE_TAG_NAME, 123)

    def test_create_or_verify_tag_color_empty_after_trim(self):
        """Test validation with whitespace-only tag color."""
        with pytest.raises(MissingTagColor, match="Tag color cannot be empty"):
            TagRegistryRepository.create_or_verify_tag(FAKE_TAG_NAME, "   ")

    def test_create_or_verify_tag_existing_no_color_field(self, mock_db):
        """Test existing tag without color field."""
        existing_tag = {
            "_id": ObjectId(FAKE_TAG_ID),
            "name": FAKE_TAG_NAME
            # No color field
        }
        with patch("database.repository.tag_registry_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.tag_registry.find_one.return_value = existing_tag

            with pytest.raises(DuplicateTagColor, match=f"Tag '{FAKE_TAG_NAME}' already exists with different color"):
                TagRegistryRepository.create_or_verify_tag(FAKE_TAG_NAME, FAKE_TAG_COLOR)

    def test_create_or_verify_tag_database_exception(self, mock_db):
        """Test handling of database exceptions during tag creation."""
        with patch("database.repository.tag_registry_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.tag_registry.find_one.side_effect = Exception("Database error")

            with pytest.raises(Exception, match="Database error"):
                TagRegistryRepository.create_or_verify_tag(FAKE_TAG_NAME, FAKE_TAG_COLOR)
