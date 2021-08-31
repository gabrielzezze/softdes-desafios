from user import User
from sqlite3 import connect


class Quiz:
    def __init__(self, quiz_id: str, user: User):
        self.quiz_id = quiz_id
        self.user = user

        db_name = environ.get("DBNAME", None)
        if db_name is None:
            raise DBNameNotFoundException()
        self.dbname = db_name

    def get(self):
        conn = connect(DBNAME)
        cursor = conn.cursor()
        if user == "admin" or user == "fabioja":
            cursor.execute(
                "SELECT id, release, expire, problem, tests, results, diagnosis, numb from QUIZ where id = {0}".format(
                    id
                )
            )
        else:
            cursor.execute(
                "SELECT id, release, expire, problem, tests, results, diagnosis, numb from QUIZ where id = {0} and release < '{1}'".format(
                    id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            )
        info = [reg for reg in cursor.fetchall()]
        conn.close()
        return info
