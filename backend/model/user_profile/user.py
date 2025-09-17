from database.repository.date_time_utils import get_utc_zulu_timestamp

class User:
    def __init__(self, user_id, first_name, last_name, email, view_mode = None, active = None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.view_mode = view_mode
        self.active = active

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

    @classmethod
    def from_dict(cls, user: dict):
        return cls(
            user_id = user.get("_id") or user.get("user_id"),
            first_name = user.get("first_name"),
            last_name = user.get("last_name"),
            email = user.get("email"),
            view_mode = user.get("view_mode"),
            active = user.get("active"),
        )
