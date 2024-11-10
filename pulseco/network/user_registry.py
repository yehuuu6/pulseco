from typing import List, Any

class UserRegistry:
    """
    Singleton class that holds all the users online.
    """
    _instance = None
    _users: List[Any] = []

    # Singleton pattern
    # This class will only have one instance.
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserRegistry, cls).__new__(cls)
        return cls._instance

    def register(self, user: Any):
        self._users.append(user)

    def get_users(self) -> List[Any]:
        return self._users

# Create a singleton instance
user_registry = UserRegistry()