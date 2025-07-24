from database.repository.date_time_utils import get_utc_zulu_timestamp
from model.user_profile.view_mode import ViewMode

class User:
    def __init__(self, user_id, first_name, last_name, email):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.prefered_mode = ViewMode.LIGHT  # by default maybe it's set to light mode

    def new_user_dict(self):
        user_dic = {
            "_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "view_mode": False,
            "active": True,

            "created_at": get_utc_zulu_timestamp(),
            "updated_at": get_utc_zulu_timestamp(),
        }
        return user_dic
