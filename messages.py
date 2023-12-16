import sqlite3
import json
from rich import print

db_path = "messages.db"
db_conn = sqlite3.connect(db_path)
cursor = db_conn.cursor()


class GroupMessageManager:
    def __init__(self):
        self.create_table()

    def create_table(self):
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS groupmsg(
                id INTEGER PRIMARY KEY,
                group_id INTEGER,
                msg_id INTEGER,
                user_id INTEGER,
                msg_text TEXT,
                extra TEXT
            );
            '''
        )
        db_conn.commit()

    def add_message(
        self, group_id: int, msg_id: int, user_id: int, msg_text: str, extra=None
    ):
        if extra:
            extra = json.dumps(extra)
        cursor.execute(
            '''
            INSERT INTO groupmsg(group_id, msg_id, user_id, msg_text, extra)
            VALUES(?, ?, ?, ?, ?);
            ''',
            (group_id, msg_id, user_id, msg_text, extra),
        )
        db_conn.commit()
        print("[green]Inserted row:[/green]", {
            "group_id": group_id,
            "msg_id": msg_id,
            "user_id": user_id,
            "msg_text": msg_text,
            "extra": extra
        })
        # if random() < 0.25:
        #     self.delete_cache(group_id)

    def get_latest_messages_by_group_id(self, group_id: int, limit=100) -> list:
        cursor.execute(
            '''
            SELECT user_id, msg_text FROM groupmsg
            WHERE group_id = ?
            ORDER BY msg_id DESC
            LIMIT ?;
            ''',
            (group_id, limit),
        )
        rows = cursor.fetchall()
        return [{"user_id": row[0], "msg_text": row[1]} for row in rows]
    
    def delete_cache(self, group_id: int):
        pass

    def test_get_latest_messages_by_group_id(self, group_id: int):
        latest_300_messages = self.get_latest_messages_by_group_id(group_id, 300)
        first_10_latest_messages = latest_300_messages[:10]
        last_10_messages = latest_300_messages[-10:]
        return first_10_latest_messages + last_10_messages

msg_manager = GroupMessageManager()
