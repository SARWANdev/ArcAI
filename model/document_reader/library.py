from model.document_reader.project import Project


class Library:
    def __init__(self):
        self.projects = []
        
    def add_project(self, project):
        self.projects.append(project)

    def delete_project(self, project):
        self.projects.remove(project)

