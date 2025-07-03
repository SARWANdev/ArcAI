from habanero import Crossref
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
import requests
 

class BibTeX_Service:

    
    def __init__(self, paper_name: str) -> None:
        self.__paper_name = paper_name
        __unformatted_bibtex_string = self.__get_bibtex_str(paper_name=paper_name)
        self.__bibtex_library = bibtexparser.loads(__unformatted_bibtex_string, parser=bibtexparser.bparser.BibTexParser())
        self.__formatted_bibtex_string = bibtexparser.dumps(bib_database=self.__bibtex_library)
        



        pass

    def __get_bibtex_str(self, paper_name:str)->str:
        cr = Crossref()
        cr.timeout=1200
        res = cr.works(query=paper_name, limit=1)
        doi = res['message']['items'][0]['DOI'] 
        bibtex_str = requests.get(f"https://doi.org/{doi}", headers={"Accept": "application/x-bibtex"}, stream=False).text
        return bibtex_str
    
    def save_to_file(self, path:str):
        id = self.__bibtex_library.entries[0].get("ID")+".bib"
        with open(path + id + ".bib", "w") as file:
            file.write(self.__formatted_bibtex_string)

    def get_bibtex_string(self)->str:
        return self.__formatted_bibtex_string

    def get_bibtex_library(self)->BibDatabase:
        return self.__bibtex_library

    def get_paper_name(self)->str:
        return self.__paper_name        


bib = BibTeX_Service("Blending Immersive Gameplay with Intense Exercise Using Asynchronous Exergaming")
bib.save_to_file(bib.get_paper_name()+".bib")
print("done")