from telegram import Message
import random


class ProgressContext:
    def __init__(self, message: Message):
        self.message = message
        self.count = 0

    def add_count(self):
        self.count += 1

    async def uploading_assets(self, text: str):
        if random.random() < 0.7:
            return

        new_text = f"Saved tweets: {self.count}\nNow uploading {text}…"
        if self.message.text == new_text:
            return
        return await self.message.edit_text(new_text)
