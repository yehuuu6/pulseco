from app.models.plugin import Plugin
from typing import List

class AnnouncementsPlugin(Plugin):
    def __init__(self):
        super().__init__(
            name="Announcements",
            description="Send messages to all the online users in the room.",
            version="1.0.0",
            author="yehuuu6",
            color="hot_pink",
        )
        self.messages: List[str] = []

    def on_load(self) -> None:
        """
        Called when the plugin is loaded.
        """
        super().on_load()
        from app.server import room
        self.room = room
        cfg = room.cfg_loader.config

        self.messages = [
            f"Welcome to the {cfg.name}!",
            "This is a test announcement.",
            "Please read the rules and guidelines.",
            "If you have any questions, feel free to ask.",
            "Enjoy your stay!",
            "Remember to be respectful to others.",
            "Have fun and make new friends!",
            "Check out our website for more information.",
        ]

        # Start announcements in a separate thread
        import threading
        announcement_thread = threading.Thread(target=self.send_announcement, daemon=True)
        announcement_thread.start()

    def send_announcement(self) -> None:
        # Pick a random message from the list, and send it in a set interval
        import random
        import time
        from app.utils.functions import printf
        while True:
            message = random.choice(self.messages)
            self.room.broadcast(message)
            printf(f"[{self.color}]Announcement sent: {message}[/]")
            time.sleep(random.randint(5, 20))  # Random interval between 5 to 20 seconds