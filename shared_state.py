
class Username:
    """Связывающий класс между main и ботом для получения имя пользователя."""

    _instance = None
    username = None
    user_id = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Username, cls).__new__(cls)
            cls._instance.username = None
        return cls._instance

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def set_user_id(self, username):
        self.user_id = username

    def get_user_id(self):
        return self.user_id


username_instance = Username()
