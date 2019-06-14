import sys
import os

sys.path.append("%s/../../lab3" % os.getcwd())

from db_generator import choose_variant_from_dict, get_input_int
import generator as dc_gnr
import statistic as dc_stat

import psycopg2
import json
import numpy as np


def pretty_print(phrase):
    print("\n-------------- %s ---------\n" % phrase)


def parse_game_params(path):
    params_dict = json.load(open(path, 'r'))

    max_time = params_dict.__getitem__("max_time")
    account = params_dict.__getitem__("account")

    return max_time, account


def try_commit(conn):
    commit_allowed = choose_variant_from_dict(title="COMMIT CHANGES?", variants={0: 'no', 1: 'yes'})
    if commit_allowed:
        conn.commit()


def store_json_for_current_game(cursor, path, account, max_time):
    cursor.execute("select id,price,value from item;")
    items = np.array(cursor.fetchall()).transpose()
    j_dict = {"ids": items[0],
              "prices": items[1],
              "values": items[2],
              "account": account,
              "max_time": max_time}

    with open(path, "w") as fp:
        json.dump(j_dict, fp)

    pass


# ----------------------- main ----------------------------------
if __name__ == '__main__':

    pretty_print("damned_capitalism launched")

    # --------------------------- initializing --------------------------------------
    pretty_print("initializing")
    dc_gnr.init_generator_params_from_json("../cfg/generator_cfg.json")

    db_name = 'damned_capitalism'
    login = "manager"
    password = '1234'

    conn = psycopg2.connect(dbname=db_name, user=login, password=password, host='localhost')
    cursor = conn.cursor()

    # ------------------------------- filling -----------------------------------------
    fill_complete = False
    while not fill_complete:

        # --------------------------- configurating --------------------------------------
        ti = choose_variant_from_dict(
            "AVAILABLE ACTIONS:",
            {0: 'new game', 1: 'show hall of fame', 9: 'exit'}
        )

        # ------------------------ new game --------------------------------------
        if ti == 0:
            dc_gnr.generate_new_game(cursor=cursor)
            try_commit(conn)
            max_time, account = parse_game_params("../cfg/game_cfg.json")
            store_json_for_current_game(cursor=cursor,
                                        path="../res/algorithms/items.json",
                                        account=account, max_time=max_time)

        if ti == 1:
            print("TODO show hall of fame")

        # ------------------------ exiting --------------------------------------
        elif ti == 9:
            pretty_print("exiting")
            fill_complete = True

    cursor.close()
    conn.close()
