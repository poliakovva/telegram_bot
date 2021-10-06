import sqlite3
from time import time
from misc import cur, con


def get_brick_by_id(brick_id: int):
    return list(cur.execute('SELECT * FROM'
                            ' brick WHERE id=?',
                            (brick_id,)))[0]


def get_edges_by_brick(brick_id: int):
    return list(cur.execute("SELECT * FROM"
                            " edges WHERE `from`=?",
                            (brick_id,)))


def get_or_create_user(tg_id: int, tg_name: str):
    user = None
    try:
        user = list(cur.execute("SELECT * FROM"
                                " users WHERE tg_id=?",
                                (tg_id,)))[0]
        return user
    except:
        cur.execute("INSERT INTO users"
                    " (tg_id, state, tg_name)"
                    " VALUES (?, ?, ?)",
                    (tg_id, get_start_brick()['id'], tg_name))
        con.commit()
        return list(cur.execute("SELECT * FROM"
                                " users WHERE tg_id=?",
                                (tg_id,)))[0]


def set_user_state(tg_id: int, brick_id: int):
    cur.execute("UPDATE users SET state=? WHERE tg_id=?",
                (brick_id, tg_id,))
    con.commit()


def get_start_brick():
    return list(cur.execute("SELECT * FROM"
                            " brick WHERE start=1"))[0]


def delete_user(tg_id: int):
    cur.execute("DELETE FROM users WHERE tg_id=?",
                (tg_id,))
    con.commit()


def add_log(tg_id: int, brick_id: int, msg: str, is_trigger: int):
    cur.execute("INSERT INTO log"
                " (tg_id, datetime, brick, msg, is_trigger)"
                " VALUES (?, ?, ?, ?, ?)",
                (tg_id, int(time()), brick_id, msg, is_trigger, ))
    con.commit()
