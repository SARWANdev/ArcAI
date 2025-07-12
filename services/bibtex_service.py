from habanero import Crossref
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
import requests
 

class BibTeX_Service:

    
    def __init__(self, paper_name: str) -> None:
        self.__paper_name = paper_name.replace("_", " ")
        __unformatted_bibtex_string = self.__get_bibtex_str(paper_name=self.__paper_name)
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
        #correct = input(f"found {title}  with simscore {similarity_score} accept this?").lower() in ("yes","y") #TODO forward this to front end
        correct = True
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


    def get_paper_name(self)->str:
        return self.__paper_name
    
    def get_bibtex_library_dict(self):
        return self.__bibtex_library.entries[0]
    
    def get_authors(self):
        author_string = self.__bibtex_library.entries[0]['author']
        authors = author_string.split(" and ")
        return authors
    
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

        pass






bibs = [BibTeX_Service("Efficient_Embedding_of_Scale-Free_Graphs_in_the_Hyperbolic_Plane"),
       BibTeX_Service("Automatic Visual Detection of Fresh Poultry Egg Quality Inspection using Image Processing"),
       BibTeX_Service("Blending Immersive Gameplay with Intense Exercise using Asynchronous Exergaming"),
       BibTeX_Service("Online Level Generation in Super Mario Bros via Learning Constructive Primitives"),
       BibTeX_Service("Quantum Mechanics")]

for bib in bibs:
    bib.save_to_file(bib.get_paper_name())
    bib_dict = bib.get_bibtex_library_dict()

    author = str(bib.get_authors())
    author1 = bib.get_author1_last_name()
    year = bib_dict['year']
    title = bib_dict['title']
    source = bib.get_source()
    print(f"Authors: {str(author)}")
    print(f"Author 1 last name: {author1}")
    print(f"publication year: {year}")
    print(f"source: {source}")
    print(f"title: {title}\n\n")


