import sqlite3
from os import environ
from typing import Any


class DBNameNotFoundException(Exception):
    pass


class User:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.is_admin = user_id in ["admin", "fabioja"]

        db_name = environ.get("DBNAME", None)
        if db_name is None:
            raise DBNameNotFoundException()
        self.dbname = db_name

    def get_user_quiz(self, quiz_id: str):
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT sent,answer,result from USERQUIZ where userid = '{0}' and quizid = {1} order by sent desc".format(
                self.user_id, quiz_id
            )
        )
        info = [reg for reg in cursor.fetchall()]
        conn.close()
        return info

    def set_user_quiz(self, quiz_id: str, sent: bool, answer: Any, results: Any):
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        cursor.execute(
            "insert into USERQUIZ(userid,quizid,sent,answer,result) values (?,?,?,?,?);",
            (self.user_id, quiz_id, sent, answer, results),
        )
        conn.commit()
        conn.close()
        return
