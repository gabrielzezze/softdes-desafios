FROM ubuntu:20.04

RUN apt update
RUN apt upgrade -y
RUN apt install python3-pip sqlite3 git -y

RUN pip3 install pipenv
RUN git clone https://github.com/gabrielzezze/softdes-desafios.git ./repo

WORKDIR /repo/

RUN pipenv install

RUN rm -rf src/quiz.db
RUN sqlite3 src/quiz.db
RUN sqlite3 src/quiz.db '.read ./src/quiz.sql'

# RUN pipenv run python3 src/adduser.py

CMD pipenv run python3 /repo/src/softdes.py