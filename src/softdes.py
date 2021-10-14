# -*- coding: utf-8 -*-
# pylint: disable=W0123
"""
Created on Wed Jun 28 09:00:39 2017

@author: rauli
"""

from datetime import datetime
import sqlite3
import hashlib
from flask import (
    Flask,
    request,
    render_template,
)
from flask_httpauth import HTTPBasicAuth

DBNAME = "./quiz.db"


def get_quizzes(user):
    """
    Get specified user quizzes release before today or if user is admin get all quizzes
    Params:
        user: User Id
    Return:
        List of quizzes
    """
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    is_user_admin = user in ["admin", "fabioja"]
    if is_user_admin:
        cursor.execute("SELECT id, numb from QUIZ")
    else:
        cursor.execute(
            "SELECT id, numb from QUIZ where release < '{0}'".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
    info = list(cursor.fetchall())
    conn.close()
    return info


def get_user_quiz(userid, quizid):
    """
    Get specified quiz of specified user
    """
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT
                sent,
                answer,
                result
            FROM
               USERQUIZ
            WHERE
                userid = '{0}' and quizid = {1}
            ORDER BY SENT DESC
        """.format(
            userid, quizid
        )
    )
    info = list(cursor.fetchall())
    conn.close()
    return info


def set_user_quiz(userid, quizid, sent, answer, result):
    """
    Submit user quiz answer
    """
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute(
        "insert into USERQUIZ(userid,quizid,sent,answer,result) values (?,?,?,?,?);",
        (userid, quizid, sent, answer, result),
    )
    conn.commit()
    conn.close()


def get_quiz(quiz_id, user):
    """
    If user is admin get all quizzes if not get quizzes available
    """
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    is_user_admin = user in ["admin", "fabioja"]
    if is_user_admin:
        cursor.execute(
            """
                SELECT
                    id,
                    release,
                    expire,
                    problem,
                    tests,
                    results,
                    diagnosis,
                    numb
                FROM
                    QUIZ
                WHERE id = {0}
            """.format(
                quiz_id
            )
        )
    else:
        cursor.execute(
            """
                SELECT
                    id,
                    release,
                    expire,
                    problem,
                    tests,
                    results,
                    diagnosis,
                    numb
                FROM
                    QUIZ
                WHERE id = {0} and release < '{1}'
            """.format(
                quiz_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
    info = list(cursor.fetchall())
    conn.close()
    return info


def set_info(pwd, user):
    """
    Set user info
    """
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE USER set pass = ? where user = ?", (pwd, user))
    conn.commit()
    conn.close()


def get_info(user):
    """
    Get User info
    """
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute("SELECT pass, type from USER where user = '{0}'".format(user))
    info = [reg[0] for reg in cursor.fetchall()]
    conn.close()
    if len(info) == 0:
        return None
    return info[0]


auth = HTTPBasicAuth()

app = Flask(__name__, static_url_path="")
app.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?TX"


@app.route("/", methods=["GET", "POST"])
@auth.login_required
def main():
    """
    Handle main page rendering depending on auth
    """
    msg = ""
    phase = 1
    challenges = get_quizzes(auth.username())
    sent = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if request.method == "POST" and "ID" in request.args:
        quiz_id = request.args.get("ID")
        quiz = get_quiz(quiz_id, auth.username())
        if len(quiz) == 0:
            msg = "Boa tentativa, mas não vai dar certo!"
            phase = 2
            return render_template(
                "index.html",
                username=auth.username(),
                challenges=challenges,
                p=phase,
                msg=msg,
            )

        quiz = quiz[0]
        if sent > quiz[2]:
            msg = "Sorry... Prazo expirado!"

        answer_file = request.files["code"]
        filename = "./src/upload/{0}-{1}.py".format(auth.username(), sent)
        answer_file.save(filename)
        with open(filename, "r", encoding="UTF-8") as file_buffer:
            answer = file_buffer.read()

        # lamb = boto3.client('lambda')
        args = {
            "ndes": quiz_id,
            "code": answer,
            "args": eval(quiz[4]),
            "resp": eval(quiz[5]),
            "diag": eval(quiz[6]),
        }

        feedback = lambda_handler(args, "")

        result = "Erro"
        if len(feedback) == 0:
            feedback = "Sem erros."
            result = "OK!"

        set_user_quiz(auth.username(), quiz_id, sent, feedback, result)

    if request.method == "GET":
        if "ID" in request.args:
            quiz_id = request.args.get("ID")
        else:
            quiz_id = 1

    if len(challenges) == 0:
        msg = "Ainda não há desafios! Volte mais tarde."
        phase = 2
        return render_template(
            "index.html",
            username=auth.username(),
            challenges=challenges,
            p=phase,
            msg=msg,
        )

    quiz = get_quiz(quiz_id, auth.username())

    if len(quiz) == 0:
        msg = "Oops... Desafio invalido!"
        phase = 2
        return render_template(
            "index.html",
            username=auth.username(),
            challenges=challenges,
            p=phase,
            msg=msg,
        )

    answers = get_user_quiz(auth.username(), quiz_id)

    return render_template(
        "index.html",
        username=auth.username(),
        challenges=challenges,
        quiz=quiz[0],
        e=(sent > quiz[0][2]),
        answers=answers,
        p=phase,
        msg=msg,
        expi=converteData(quiz[0][2]),
    )


@app.route("/pass", methods=["GET", "POST"])
@auth.login_required
def change():
    """
    Handle page rendering for password change
    """
    if request.method == "POST":
        velha = request.form["old"]
        nova = request.form["new"]
        repet = request.form["again"]

        phase = 1
        msg = ""
        if nova != repet:
            msg = "As novas senhas nao batem"
            phase = 3
        elif get_info(auth.username()) != hashlib.md5(velha.encode()).hexdigest():
            msg = "A senha antiga nao confere"
            phase = 3
        else:
            set_info(hashlib.md5(nova.encode()).hexdigest(), auth.username())
            msg = "Senha alterada com sucesso"
            phase = 3
    else:
        msg = ""
        phase = 3

    return render_template(
        "index.html",
        username=auth.username(),
        challenges=get_quizzes(auth.username()),
        p=phase,
        msg=msg,
    )


@app.route("/logout")
def logout():
    """
    Handle logout page rendering
    """
    return render_template("index.html", p=2, msg="Logout com sucesso"), 401


@auth.get_password
def get_password(username):
    """
    Get user password
    """
    return get_info(username)


@auth.hash_password
def hash_pw(password):
    """
    Handle password string hashing
    """
    return hashlib.md5(password.encode()).hexdigest()

def lambda_handler(event, context):
    try:
        import json
        import numbers

        def not_equals(first, second):
            if isinstance(first, numbers.Number) and isinstance(second, numbers.Number):
                return abs(first - second) > 1e-3
            return first != second

        # TODO implement
        ndes = int(event["ndes"])
        code = event["code"]
        args = event["args"]
        resp = event["resp"]
        diag = event["diag"]
        exec(code, locals())

        test = []
        for index, arg in enumerate(args):
            if not "desafio{0}".format(ndes) in locals():
                return "Nome da função inválido. Usar 'def desafio{0}(...)'".format(
                    ndes
                )

            if not_equals(eval("desafio{0}(*arg)".format(ndes)), resp[index]):
                test.append(diag[index])

        return " ".join(test)
    except:
        return "Função inválida."


def converteData(orig):
    return (
        orig[8:10]
        + "/"
        + orig[5:7]
        + "/"
        + orig[0:4]
        + " "
        + orig[11:13]
        + ":"
        + orig[14:16]
        + ":"
        + orig[17:]
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
