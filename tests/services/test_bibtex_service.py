import pytest
from services.bibtex_service import BibTeX_Service
from exceptions.bibtex_exceptions import BibTeXParseException

@pytest.fixture
def valid_bibtex():
    return """@article{sample2020, author = {John Doe and Jane Smith}, title = {Sample Paper}, year = {2020}, journal = {Journal of Testing}}"""

@pytest.fixture
def invalid_bibtex():
    return "@article{sample2020, author = John Doe, title = Sample Paper, year = 2020, journal = Journal of Testing}"

def test_parse_valid_bibtex(valid_bibtex):
    service = BibTeX_Service()
    result = service.set_bibtex(valid_bibtex)
    assert result is True
    assert service.get_title() == "Sample Paper"
    assert service.get_first_author() == "John Doe"
    assert service.get_year() == "2020"
    assert service.get_source() == "Journal of Testing"


def test_get_bibtex_string(valid_bibtex):
    service = BibTeX_Service()
    service.set_bibtex(valid_bibtex)
    bibtex_str = service.get_bibtex_string()
    assert bibtex_str is not None
    assert "@article" in bibtex_str
    assert "Sample Paper" in bibtex_str

def test_get_authors(valid_bibtex):
    service = BibTeX_Service()
    service.set_bibtex(valid_bibtex)
    authors = service.get_authors()
    assert authors == ["John Doe", "Jane Smith"]

def test_get_bibtex_library_dict(valid_bibtex):
    service = BibTeX_Service()
    service.set_bibtex(valid_bibtex)
    bib_dict = service.get_bibtex_library_dict()
    assert bib_dict is not None
    assert isinstance(bib_dict, dict)
    assert bib_dict.get("title") == "Sample Paper"

def test_parse_bibtex_invalid_format(bibtex_service):
    invalid_bibtex = "@article{bad, title = {Missing end brace}"
    with pytest.raises(BibTeXParseException):
        bibtex_service.parse_bibtex(invalid_bibtex)


def test_delete_bibtex_entry_not_found(bibtex_service):
    with pytest.raises(BibTeXParseException):
        bibtex_service.delete_bibtex_entry('notfound')

def test_update_bibtex_entry_not_found(bibtex_service):
    entry = {'id': 'notfound', 'title': 'Missing'}
    with pytest.raises(BibTeXParseException):
        bibtex_service.update_bibtex_entry(entry)


def test_get_bibtex_entry_not_found(bibtex_service):
    with pytest.raises(BibTeXParseException):
        bibtex_service.get_bibtex_entry('notfound')

def test_import_bibtex_file_not_found(bibtex_service):
    with pytest.raises(FileNotFoundError):
        bibtex_service.import_bibtex('nonexistent.bib')

def test_save_bibtex_entry_success(bibtex_service):
    entry = {'id': 'new', 'title': 'New Entry'}
    bibtex_service.entries = {}
    bibtex_service.save_bibtex_entry(entry)
    assert 'new' in bibtex_service.entries

def test_update_bibtex_entry_success(bibtex_service):
    entry = {'id': 'update', 'title': 'Old'}
    bibtex_service.entries = {'update': entry}
    updated = {'id': 'update', 'title': 'New'}
    bibtex_service.update_bibtex_entry(updated)
    assert bibtex_service.entries['update']['title'] == 'New'
