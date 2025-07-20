from habanero import Crossref
import bibtexparser
import requests
 

class BibTeX_Service:

    # gotta clean up on frontend connection
    def __init__(self, pdf_hash, paper_name = None) -> None:
        if paper_name:
            self.pdf_hash = pdf_hash
            self.__paper_name = paper_name.replace("_", " ")
            if self.__paper_name.lower().endswith('.pdf'):
                self.__paper_name = self.__paper_name[:-4]
            __unformatted_bibtex_string = self.__get_bibtex_str(paper_name=self.__paper_name)
            if __unformatted_bibtex_string:        
                self.__bibtex_library = bibtexparser.loads(__unformatted_bibtex_string, parser=bibtexparser.bparser.BibTexParser())
                self.formatted_bibtex_string = bibtexparser.dumps(bib_database=self.__bibtex_library)
                return

        
        
    def set_bibtex(self, bibtex:str):
        self.__bibtex_library = bibtexparser.loads(bibtex, parser=bibtexparser.bparser.BibTexParser())
        self.formatted_bibtex_string = bibtexparser.dumps(bib_database=self.__bibtex_library)

    def create_misc_bibtex(self, author:str, title:str, year:int, citekey:str):
        bibtex = f"@misc{{{citekey}, author = {{{author}}}, title = {{{title}}}, year = {{{year}}}}}"
        return bibtex
        

    def get_bibtex_str(self, paper_name:str):
        cr = Crossref()
        cr.timeout=1200
        res = cr.works(query=paper_name, limit=1)
        doi = res['message']['items'][0]['DOI']
        bibtex = requests.get(f"https://doi.org/{doi}", headers={"Accept": "application/x-bibtex"}, stream=False)
        return bibtex.text
        
            
    
    def save_to_file(self):
        path = "F:/PSE/arcai/services/bibtex/"
        id = self.__bibtex_library.entries[0].get("ID")
        with open(path + self.pdf_hash + ".bib", "w") as file:
            file.write(self.formatted_bibtex_string)
            
    def get_file(self, path:str):
        id = self.__bibtex_library.entries[0].get("ID")
        with open(path + id + ".bib", "w") as file:
            return file

    def get_bibtex_string(self)->str:
        return self.formatted_bibtex_string

    def get_paper_name(self)->str:
        return self.__paper_name
    
    def get_bibtex_library_dict(self):
        return self.__bibtex_library.entries[0]
    
    def get_authors(self):
        author_string = self.__bibtex_library.entries[0]['author']
        authors = author_string.split(" and ")
        return str(authors)
    
    def get_author1_last_name(self):
        authors = self.get_authors()
        author1 = authors[0]
        return author1.split(", ")[0]
    
    def get_source(self):
        bib_dict = self.get_bibtex_library_dict()
        source_fields = ['booktitle', 'journal', 'series', 'school']
        for field in source_fields:
            if field in bib_dict and bib_dict[field]:
                return bib_dict[field]

    
    def get_year(self):
        return self.get_bibtex_library_dict()['year']   
    
from upload_manager.hash_manager import get_pdf_sha256
b = BibTeX_Service(pdf_hash = get_pdf_sha256("papers/Automatic_Visual_Detection_of_Fresh_Poultry_Egg_Quality_Inspection_using_Image_Processing.pdf"), 
                   paper_name="Automatic Visual Detection of Fresh Poultry Egg Quality Inspection using Image Processing")
b.save_to_file()
