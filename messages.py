from peewee import *
from rich import print
from random import random
import json

db = SqliteDatabase("messages.db")


class GroupMessageTable(Model):
    group_id = IntegerField()
    msg_id = IntegerField()
    user_id = IntegerField()
    msg_text = TextField()
    extra = TextField(null=True)

    class Meta:
        database = db


class GroupMessageManager:
    def __init__(self):
        self.table = GroupMessageTable()
        self.create_table()

    def create_table(self):
        with db:
            self.table.create_table()

    def add_message(
        self, group_id: int, msg_id: int, user_id: int, msg_text: str, extra=None
    ):
        if extra:
            extra = json.dumps(extra)
        message = self.table.create(
            group_id=group_id,
            msg_id=msg_id,
            user_id=user_id,
            msg_text=msg_text,
            extra=extra,
        )
        print("[green]Inserted row:[/green]", message)
        if random() < 0.25:
            self.delete_cache(group_id)
        return message

    def get_latest_messages_by_group_id(self, group_id: int, limit=100):
        # write a method that fetches 100 latest messages in table by group_id. in a group, the lager msg_id is, the newer the message is.
        messages = (
            self.table.select()
            .where(self.table.group_id == group_id)
            .order_by(self.table.msg_id)
            .limit(limit)
        )
        return messages

    def delete_cache(self, group_id: int):
        pass

    def test_get_latest_messages_by_group_id(self, group_id: int):
        # write a method that returns a list of the first 10 latest messages and the last 10 of the result of the 300 latest messages.
        latest_300_messages = self.get_latest_messages_by_group_id(group_id)
        first_10_latest_messages = latest_300_messages[:10]
        last_10_messages = latest_300_messages[-10:]
        return list(first_10_latest_messages) + list(last_10_messages)

msg_manager = GroupMessageManager()