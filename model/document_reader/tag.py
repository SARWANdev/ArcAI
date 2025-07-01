class Tag:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def rename_tag(self, name):
        self.name = name

    def set_color(self, color):
        self.color = color
