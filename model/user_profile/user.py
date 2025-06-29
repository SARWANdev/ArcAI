from model.user_profile.view_mode import ViewMode

class User:
    def __init__(self, user_id, first_name, last_name, email):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.prefered_mode = ViewMode.LIGHT  # by default maybe it's set to light mode
