import sys
import os

sys.path.append("%s/../../lab3" % os.getcwd())

from db_generator import choose_variant_from_dict, get_input_int
import generator as dcgen
import statistic as dcstat
import algorithms_runer as dcar

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


def delete_out_files():
    alg_dir = "../algorithms"
    os.system("rm -f %s/items.json" % alg_dir)
    for alg in os.listdir(alg_dir):
        os.system("rm -f %s/%s/answer.json" % (alg_dir, alg))


def init_stored_procedures(cursor):
    st_proc_dir = "../db/stored_procedures"
    for sql_file in os.listdir(st_proc_dir):
        req = ""
        for line in open("%s/%s" % (st_proc_dir, sql_file)).readlines():
            req += line
        print("init %s/%s" % (st_proc_dir, sql_file))
        cursor.execute(req)


def store_json_for_current_game(cursor, path, account, max_time):
    cursor.execute("select id,price,value from item;")
    items = np.array(cursor.fetchall()).transpose().astype(int)
    j_dict = {"ids": list(items[0]),
              "prices": list(items[1]),
              "values": list(items[2]),
              "account": account,
              "max_time": max_time}

    with open(path, "w") as fp:
        json.dump(j_dict, fp, default=int)  # best bone in my life

    pass


# ----------------------- main ----------------------------------
if __name__ == '__main__':

    pretty_print("damned_capitalism launched")

    # --------------------------- initializing --------------------------------------
    pretty_print("initializing of data generator")
    dcgen.init_generator_params_from_json("../cfg/generator_cfg.json")

    pretty_print("db connecting")
    db_name = 'damned_capitalism'
    login = "manager"
    password = '1234'

    conn = psycopg2.connect(dbname=db_name, user=login, password=password, host='localhost')
    cursor = conn.cursor()

    pretty_print("initializing of stored procedures ")
    init_stored_procedures(cursor)

    conn.commit()

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
            dcgen.generate_new_game(cursor=cursor)
            conn.commit()
            max_time, account = parse_game_params("../cfg/game_cfg.json")
            store_json_for_current_game(cursor=cursor,
                                        path="../algorithms/items.json",
                                        account=account, max_time=max_time)
            dcar.run_all(cursor, "../cfg/game_algorithms.json", max_time=max_time)
            conn.commit()
            dcstat.show_results(cursor)

        if ti == 1:
            print("TODO show hall of fame")

        # ------------------------ exiting --------------------------------------
        elif ti == 9:
            pretty_print("exiting")
            delete_out_files()
            fill_complete = True

    cursor.close()
    conn.close()
