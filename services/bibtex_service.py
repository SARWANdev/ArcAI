from habanero import Crossref
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
import requests
 

class BibTeX_Service:

    
    def __init__(self, paper_name: str) -> None:
        self.__paper_name = paper_name
        __unformatted_bibtex_string = self.__get_bibtex_str(paper_name=paper_name)
        if __unformatted_bibtex_string:
            self.__bibtex_library = bibtexparser.loads(__unformatted_bibtex_string, parser=bibtexparser.bparser.BibTexParser())
            self.__formatted_bibtex_string = bibtexparser.dumps(bib_database=self.__bibtex_library)
        



        

    def __get_bibtex_str(self, paper_name:str)->str:
        cr = Crossref()
        cr.timeout=1200
        res = cr.works(query=paper_name, limit=1)
        similarity_score = res['message']['items'][0]['score']
        doi = res['message']['items'][0]['DOI']
        title = res['message']['items'][0]['title']
        correct = input(f"found {title}  with simscore {similarity_score} accept this?").lower() in ("yes","y") #TODO forward this to front end
        if correct:
            doi = res['message']['items'][0]['DOI'] 
            bibtex = requests.get(f"https://doi.org/{doi}", headers={"Accept": "application/x-bibtex"}, stream=False)
            return bibtex.text
    
    def save_to_file(self, path:str):
        id = self.__bibtex_library.entries[0].get("ID")
        with open(path + id + ".bib", "w") as file:
            file.write(self.__formatted_bibtex_string)

    def get_bibtex_string(self)->str:
        return self.__formatted_bibtex_string

    def get_bibtex_library(self)->BibDatabase:
        return self.__bibtex_library

    def get_paper_name(self)->str:
        return self.__paper_name
    
    def get_bibtex_library(self):
        return self.__bibtex_library



bib = BibTeX_Service("Online Level Generation in Super Mario Bros via Learning Constructive Primitives")
bib.save_to_file(bib.get_paper_name())
library = bib.get_bibtex_library()
print(library.entries_dict)
