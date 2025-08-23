from habanero import Crossref
import bibtexparser
import requests
import os
from typing import Optional, Dict, Any
from exceptions.bibtex_exceptions import BibTeXParseException, BibTeXSaveException

class BibTeX_Service:
    """
    Service for handling BibTeX data retrieval, parsing, and file management.
    """

    def __init__(self, pdf_hash: Optional[str] = None, paper_name: Optional[str] = None) -> None:
        """
        Initialize BibTeX_Service with either a paper name to search for or just a pdf_hash.

        :param pdf_hash: Hash of the associated PDF file.
        :type pdf_hash: str, optional
        :param paper_name: Name of the paper to search for.
        :type paper_name: str, optional
        :return: None
        :rtype: None
        """
        self.pdf_hash = pdf_hash
        self.__paper_name = None
        self.__bibtex_library = None
        self.formatted_bibtex_string = None
        if paper_name:
            self._process_paper_name(paper_name)

    def _process_paper_name(self, paper_name: str) -> None:
        """
        Process the paper name and attempt to fetch BibTeX data.

        :param paper_name: The name of the paper to process.
        :type paper_name: str
        :return: None
        :rtype: None
        """
        try:
            self.__paper_name = paper_name.replace("_", " ")
            if self.__paper_name.lower().endswith('.pdf'):
                self.__paper_name = self.__paper_name[:-4]
            unformatted_bibtex_string = self.get_bibtex_str(self.__paper_name)
            if unformatted_bibtex_string:
                self._parse_bibtex(unformatted_bibtex_string)
            else:
                print(f"No BibTeX data found for: {self.__paper_name}")
        except Exception as e:
            print(f"Error processing paper name '{paper_name}': {e}")

    def _parse_bibtex(self, bibtex_string: str) -> None:
        """
        Parse BibTeX string and format it.

        :param bibtex_string: The BibTeX string to parse.
        :type bibtex_string: str
        :return: None
        :rtype: None
        """
        try:
            self.__bibtex_library = bibtexparser.loads(
                bibtex_string, 
                parser=bibtexparser.bparser.BibTexParser()
            )
            self.formatted_bibtex_string = bibtexparser.dumps(bib_database=self.__bibtex_library)
        except Exception as e:
            self.__bibtex_library = None
            self.formatted_bibtex_string = None
            raise BibTeXParseException()

    @classmethod
    def from_bibtex(cls, bibtex_string: str, pdf_hash: Optional[str] = None):
        """
        Create BibTeX_Service instance from existing BibTeX string.

        :param bibtex_string: The BibTeX content as a string.
        :type bibtex_string: str
        :param pdf_hash: Hash of the associated PDF file.
        :type pdf_hash: str, optional
        :return: A new instance with the provided BibTeX data.
        :rtype: BibTeX_Service
        """
        instance = cls(pdf_hash=pdf_hash)
        instance.set_bibtex(bibtex_string)
        return instance

    def set_bibtex(self, bibtex: str) -> bool:
        """
        Set BibTeX data from string.

        :param bibtex: BibTeX content as string.
        :type bibtex: str
        :return: True if successful, False otherwise.
        :rtype: bool
        """
        try:
            self._parse_bibtex(bibtex)
            if self.__bibtex_library and self.__bibtex_library.entries:
                self.__paper_name = self.__bibtex_library.entries[0].get('title', '')
            return True
        except Exception as e:
            raise BibTeXParseException("Error parsing and saving BibTex")

    def get_bibtex_str(self, paper_name: str) -> Optional[str]:
        """
        Fetch BibTeX string from Crossref API.

        :param paper_name: Name of the paper to search for.
        :type paper_name: str
        :return: BibTeX string if found, None otherwise.
        :rtype: str or None
        """
        try:
            cr = Crossref()
            cr.timeout = 1200
            res = cr.works(query=paper_name, limit=1)
            if not res['message']['items']:
                print(f"No results found for: {paper_name}")
                return None
            doi = res['message']['items'][0]['DOI']
            response = requests.get(
                f"https://doi.org/{doi}", 
                headers={"Accept": "application/x-bibtex"}, 
                stream=False,
                timeout=30
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Network error fetching BibTeX for '{paper_name}': {e}")
            return None
        except KeyError as e:
            print(f"Unexpected API response format: {e}")
            return None
        except Exception as e:
            print(f"Error fetching BibTeX for '{paper_name}': {e}")
            return None

    def save_to_file(self, custom_path: Optional[str] = None) -> bool:
        """
        Save BibTeX to file.

        :param custom_path: Custom directory path to save file.
        :type custom_path: str, optional
        :return: True if successful, False otherwise.
        :rtype: bool
        """
        if not self._has_valid_data() or not self.formatted_bibtex_string:
            print("No valid BibTeX data to save")
            return False
        try:
            path = custom_path or "F:/PSE/arcai/services/bibtex/"
            os.makedirs(path, exist_ok=True)
            filename = self.pdf_hash if self.pdf_hash else "default"
            file_path = os.path.join(path, f"{filename}.bib")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.formatted_bibtex_string)
            print(f"BibTeX saved to: {file_path}")
            return True
        except Exception as e:
            print(f"Error saving BibTeX file: {e}")
            return False

    def get_file(self) -> Optional[str]:
        """
        Get the BibTeX file content as string.

        :return: BibTeX content if available, None otherwise.
        :rtype: str or None
        """
        if not self._has_valid_data():
            return None
        return self.formatted_bibtex_string

    def get_bibtex_string(self) -> Optional[str]:
        """
        Get formatted BibTeX string.

        :return: The formatted BibTeX string if available, None otherwise.
        :rtype: str or None
        """
        return self.formatted_bibtex_string

    def get_paper_name(self) -> Optional[str]:
        """
        Get paper name.

        :return: The paper name if available, None otherwise.
        :rtype: str or None
        """
        return self.__paper_name

    def get_bibtex_library_dict(self) -> Optional[Dict[str, Any]]:
        """
        Get first BibTeX entry as dictionary.

        :return: The first BibTeX entry as a dictionary if available, None otherwise.
        :rtype: dict or None
        """
        if not self._has_valid_data() or not self.__bibtex_library:
            return None
        return self.__bibtex_library.entries[0]

    def get_authors(self) -> Optional[list]:
        """
        Get list of authors.

        :return: List of author names if available, None otherwise.
        :rtype: list or None
        """
        try:
            bib_dict = self.get_bibtex_library_dict()
            if not bib_dict or 'author' not in bib_dict:
                return None
            author_string = bib_dict['author']
            authors = author_string.split(" and ")
            return [author.strip() for author in authors]
        except Exception as e:
            print(f"Error parsing authors: {e}")
            return None

    def get_first_author(self) -> Optional[str]:
        """
        Get first author name.

        :return: The first author name if available, None otherwise.
        :rtype: str or None
        """
        authors = self.get_authors()
        return authors[0] if authors else None

    def get_source(self) -> Optional[str]:
        """
        Get publication source (journal, booktitle, etc.).

        :return: The publication source if available, None otherwise.
        :rtype: str or None
        """
        try:
            bib_dict = self.get_bibtex_library_dict()
            if not bib_dict:
                return None
            source_fields = ['booktitle', 'journal', 'series', 'school']
            for field in source_fields:
                if field in bib_dict and bib_dict[field]:
                    return bib_dict[field]
            return None
        except Exception as e:
            print(f"Error getting source: {e}")
            return None

    def get_year(self) -> Optional[str]:
        """
        Get publication year.

        :return: The publication year if available, None otherwise.
        :rtype: str or None
        """
        try:
            bib_dict = self.get_bibtex_library_dict()
            return bib_dict.get('year') if bib_dict else None
        except Exception as e:
            print(f"Error getting year: {e}")
            return None

    def create_misc_bibtex(self, author: str, title: str, year: int, citekey: str) -> str:
        """
        Create a basic misc BibTeX entry.

        :param author: Author name.
        :type author: str
        :param title: Paper title.
        :type title: str
        :param year: Publication year.
        :type year: int
        :param citekey: Citation key.
        :type citekey: str
        :return: BibTeX entry as string.
        :rtype: str
        """
        return f"@misc{{{citekey}, author = {{{author}}}, title = {{{title}}}, year = {{{year}}}}}"

    def _has_valid_data(self) -> bool:
        """
        Check if instance has valid BibTeX data.

        :return: True if valid BibTeX data is present, False otherwise.
        :rtype: bool
        """
        return (
            self.__bibtex_library is not None
            and isinstance(self.__bibtex_library.entries, list)
            and len(self.__bibtex_library.entries) > 0
            and self.formatted_bibtex_string is not None
        )
    
    def get_title(self):
        """
        Get the title of the paper.

        :return: The title of the paper if available, None otherwise.
        :rtype: str or None
        """
        if self.__bibtex_library is None or not self.__bibtex_library.entries or not self._has_valid_data():
            return None
        return self.__bibtex_library.entries[0].get('title', None)


