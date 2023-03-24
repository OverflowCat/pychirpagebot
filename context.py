from telegram import Message, Update, InputMediaPhoto, InputMediaVideo
import random


class FakeProgressContext:
    def __init__(self):
        self.message = None
        self.update = None
        self.count = 0
        self.more_than_30 = False
        self.tweet_id = -1
        self.sent_desired = False
        return

    def add_count(self):
        return

    async def uploading_assets(self, text: str):
        return

    async def got_desired_tweet(self, **kwargs):
        pass


class ProgressContext:
    def __init__(self, message: Message, update: Update, tweet_id: int = 0):
        self.message = message
        self.update = update
        self.count = 0
        self.more_than_30 = False
        self.tweet_id = tweet_id
        self.sent_desired = False

    def add_count(self):
        self.count += 1

    async def uploading_assets(self, text: str):
        if self.sent_desired:
            return

        if self.more_than_30:
            return
        elif self.count >= 30:
            self.more_than_30 = True
            pass
        elif random.random() < 0.7:
            return

        new_text = f"Saved tweets: {self.count}\nNow uploading {text}…"
        if self.message.text == new_text:
            return
        if random.random() < 0.5:
            await self.message.edit_text(new_text)

    async def got_desired_tweet(self, tweet, media: list[str] | str | None):
        caption = f"""@{tweet.user.screen_name} on Twitter:
{tweet.full_text}
https://vxtwitter.com/{tweet.user.screen_name}/status/{tweet.id_str}"""
        if media is None:
            await self.update.message.reply_text(caption, quote=True)
        elif isinstance(media, list):
            media = list(map(InputMediaPhoto, media))
        elif isinstance(media, str):
            media = [InputMediaVideo(media)]
        else:
            raise ValueError("Invalid media type")
        await self.update.message.reply_media_group(media, caption=caption, quote=True)
        self.sent_desired = True
        # await self.message.delete()
