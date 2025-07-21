import os, sys
# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from services.ai_service import AIService

self = AIService()
messages = "{role:user}{boig cocks indian}"
merged_bibtex="""@misc{Butler_2018,
 author = {Butler, Leon, Santago},
 doi = {10.5040/9781350101272.00000005},
 isbn = {9781350101272},
 journal = {All You Need Is LSD 2},
 publisher = {Bloomsbury Methuen Drama},
 title = {All You Need Is LSD},
 url = {http://dx.doi.org/10.5040/9781350101272.00000005},
 year = {2019}
}
@inproceedings{Mindoro_2022,
 author = {Mindoro, Jennalyn N. and Malbog, Mon Arjay F. and Enriquez, Jennifer B. and Marasigan, Rufo and Nipas, Marte DS},
 booktitle = {2022 IEEE 13th Control and System Graduate Research Colloquium (ICSGRC)},
 doi = {10.1109/icsgrc55096.2022.9845145},
 month = {July},
 pages = {192�197},
 publisher = {IEEE},
 title = {Automatic Visual Detection of Fresh Poultry Egg Quality Inspection using Image Processing},
 url = {http://dx.doi.org/10.1109/icsgrc55096.2022.9845145},
 year = {2022}
}
@article{Blasius_2018,
 author = {Blasius, Thomas and Friedrich, Tobias and Krohmer, Anton and Laue, Soren},
 doi = {10.1109/tnet.2018.2810186},
 issn = {1558-2566},
 journal = {IEEE/ACM Transactions on Networking},
 month = {April},
 number = {2},
 pages = {920�933},
 publisher = {Institute of Electrical and Electronics Engineers (IEEE)},
 title = {Efficient Embedding of Scale-Free Graphs in the Hyperbolic Plane},
 url = {http://dx.doi.org/10.1109/tnet.2018.2810186},
 volume = {26},
 year = {2018}
}

"""

prompt = f"""1. Make a Title for a Conversation with the following human messages:{messages} Make sure that the generated title REFERENCES THE GIVEN MESSAGES. Except if the message is a greeting.
                     2. The Question was asked in the context of multiple documents. Here is the merged bibtex of all the documents: {merged_bibtex} make sure that the title has a simple reference to the multiple papers in the context.
                    3. Make sure that the conversation references the Documents and is very strongly linked to the User Message.
                    4. Only give one output without any extra information because your response will be used without any further checks in the backend
                    5. Make the title scientific and concise and between 10 to 15 words
                    6. Dont say user in the title
                    7. Dont merge different paper titles or information in the title wehn referencing multiple publications make sure that they stay seperate
                    8. Reference the user message except if its a greeting, make sure to reference it especially if it doesn't make sense in the context
                    9. Return the response without quotes
                    """

response = self.generate(prompt=prompt)
name = self.output_streaming_response(response=response, output_function=len, mode="generate")
print(name)