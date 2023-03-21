from telegram import Message
import random

class FakeProgressContext:
    def __init__(self):
        return
    def add_count(self):
        return
    async def uploading_assets(self, text: str):
        return

class ProgressContext:
    def __init__(self, message: Message):
        self.message = message
        self.count = 0
        self.more_than_30 = False

    def add_count(self):
        self.count += 1

    async def uploading_assets(self, text: str):
        if not self.more_than_30:
            if self.count >= 30:
                self.more_than_30 = True
                pass
            elif random.random() < 0.8:
                return

        new_text = f"Saved tweets: {self.count}\nNow uploading {text}…"
        if self.message.text == new_text:
            return
        return await self.message.edit_text(new_text)
