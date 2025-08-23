import pytest
from services.bibtex_service import BibTeX_Service
from exceptions.bibtex_exceptions import BibTeXParseException, BibTeXSaveException, BibTeXNotFoundException

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
