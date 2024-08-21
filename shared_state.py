
class Username:
    """Связывающий класс между main и ботом для получения имя пользователя."""

    _instance = None
    username = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Username, cls).__new__(cls)
            cls._instance.username = None
        return cls._instance

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username


username_instance = Username()
