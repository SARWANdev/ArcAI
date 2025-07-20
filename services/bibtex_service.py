from habanero import Crossref
import bibtexparser
import requests
import os
from typing import Optional, Dict, Any

class BibTeX_Service:

    def __init__(self, pdf_hash: Optional[str] = None, paper_name: Optional[str] = None) -> None:
        """
        Initialize BibTeX_Service with either a paper name to search for or just a pdf_hash.
        
        Args:
            pdf_hash (str, optional): Hash of the associated PDF file
            paper_name (str, optional): Name of the paper to search for
        """
        self.pdf_hash = pdf_hash
        self.__paper_name = None
        self.__bibtex_library = None
        self.formatted_bibtex_string = None
        
        if paper_name:
            self._process_paper_name(paper_name)

    def _process_paper_name(self, paper_name: str) -> None:
        """Process the paper name and attempt to fetch BibTeX data."""
        try:
            # Clean up paper name
            self.__paper_name = paper_name.replace("_", " ")
            if self.__paper_name.lower().endswith('.pdf'):
                self.__paper_name = self.__paper_name[:-4]
            
            # Attempt to get BibTeX string
            unformatted_bibtex_string = self.get_bibtex_str(self.__paper_name)
            if unformatted_bibtex_string:
                self._parse_bibtex(unformatted_bibtex_string)
            else:
                print(f"No BibTeX data found for: {self.__paper_name}")
                
        except Exception as e:
            print(f"Error processing paper name '{paper_name}': {e}")

    def _parse_bibtex(self, bibtex_string: str) -> None:
        """Parse BibTeX string and format it."""
        try:
            self.__bibtex_library = bibtexparser.loads(
                bibtex_string, 
                parser=bibtexparser.bparser.BibTexParser()
            )
            self.formatted_bibtex_string = bibtexparser.dumps(bib_database=self.__bibtex_library)
        except Exception as e:
            print(f"Error parsing BibTeX: {e}")
            self.__bibtex_library = None
            self.formatted_bibtex_string = None

    @classmethod
    def from_bibtex(cls, bibtex_string: str, pdf_hash: Optional[str] = None):
        """
        Create BibTeX_Service instance from existing BibTeX string.
        
        Args:
            bibtex_string (str): The BibTeX content as a string
            pdf_hash (str, optional): Hash of the associated PDF file
            
        Returns:
            BibTeX_Service: A new instance with the provided BibTeX data
        """
        instance = cls(pdf_hash=pdf_hash)
        instance.set_bibtex(bibtex_string)
        return instance

    def set_bibtex(self, bibtex: str) -> bool:
        """
        Set BibTeX data from string.
        
        Args:
            bibtex (str): BibTeX content as string
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._parse_bibtex(bibtex)
            
            # Extract paper name from title if available
            if self.__bibtex_library and self.__bibtex_library.entries:
                self.__paper_name = self.__bibtex_library.entries[0].get('title', '')
            
            return True
        except Exception as e:
            print(f"Error setting BibTeX: {e}")
            return False

    def get_bibtex_str(self, paper_name: str) -> Optional[str]:
        """
        Fetch BibTeX string from Crossref API.
        
        Args:
            paper_name (str): Name of the paper to search for
            
        Returns:
            str or None: BibTeX string if found, None otherwise
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
        
        Args:
            custom_path (str, optional): Custom directory path to save file
            
        Returns:
            bool: True if successful, False otherwise
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
        
        Returns:
            str or None: BibTeX content if available, None otherwise
        """
        if not self._has_valid_data():
            return None
        return self.formatted_bibtex_string

    def get_bibtex_string(self) -> Optional[str]:
        """Get formatted BibTeX string."""
        return self.formatted_bibtex_string

    def get_paper_name(self) -> Optional[str]:
        """Get paper name."""
        return self.__paper_name

    def get_bibtex_library_dict(self) -> Optional[Dict[str, Any]]:
        """Get first BibTeX entry as dictionary."""
        if not self._has_valid_data() or not self.__bibtex_library:
            return None
        return self.__bibtex_library.entries[0]

    def get_authors(self) -> Optional[list]:
        """
        Get list of authors.
        
        Returns:
            list or None: List of author names if available, None otherwise
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
        """Get first author name."""
        authors = self.get_authors()
        return authors[0] if authors else None

    def get_source(self) -> Optional[str]:
        """Get publication source (journal, booktitle, etc.)."""
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
        """Get publication year."""
        try:
            bib_dict = self.get_bibtex_library_dict()
            return bib_dict.get('year') if bib_dict else None
        except Exception as e:
            print(f"Error getting year: {e}")
            return None

    def create_misc_bibtex(self, author: str, title: str, year: int, citekey: str) -> str:
        """
        Create a basic misc BibTeX entry.
        
        Args:
            author (str): Author name
            title (str): Paper title  
            year (int): Publication year
            citekey (str): Citation key
            
        Returns:
            str: BibTeX entry as string
        """
        return f"@misc{{{citekey}, author = {{{author}}}, title = {{{title}}}, year = {{{year}}}}}"

    def _has_valid_data(self) -> bool:
        """Check if instance has valid BibTeX data."""
        return (
            self.__bibtex_library is not None
            and isinstance(self.__bibtex_library.entries, list)
            and len(self.__bibtex_library.entries) > 0
            and self.formatted_bibtex_string is not None
        )

# Example usage (move to separate test file in production)
if __name__ == "__main__":
    try:
        from upload_manager.hash_manager import get_pdf_sha256
        
        pdf_path = "papers/Automatic_Visual_Detection_of_Fresh_Poultry_Egg_Quality_Inspection_using_Image_Processing.pdf"
        paper_title = "Automatic Visual Detection of Fresh Poultry Egg Quality Inspection using Image Processing"
        
        # Create service instance
        bib_service = BibTeX_Service(
            pdf_hash=get_pdf_sha256(pdf_path),
            paper_name=paper_title
        )
        bib_bervice = BibTeX_Service.from_bibtex(bibtex_string="""@misc{Butler_2018,
            author = {Butler, Leon, Santago},
            doi = {10.5040/9781350101272.00000005},
            isbn = {9781350101272},
            journal = {All You Need Is LSD 2},
            publisher = {Bloomsbury Methuen Drama},
            title = {All You Need Is LSD},
            url = {http://dx.doi.org/10.5040/9781350101272.00000005},
            year = {2019}
            }
            """, pdf_hash="lol")
        
        # Save to file
        success = bib_service.save_to_file()
        buccess = bib_bervice.save_to_file()
        if success:
            print(f"Successfully processed: {bib_service.get_paper_name()}")
        else:
            print("Failed to process BibTeX data")
            
    except ImportError:
        print("hash_manager module not available for testing")
    except Exception as e:
        print(f"Error in example usage: {e}")