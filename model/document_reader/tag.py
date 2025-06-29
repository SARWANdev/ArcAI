class Tag:
    def __init__(self, name):
        self.name = name
        self.color = None

    def rename_tag(self, name):
        self.name = name

    def set_color(self, color):
        self.color = color
