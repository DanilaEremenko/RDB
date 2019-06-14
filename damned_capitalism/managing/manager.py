import sys
import os

sys.path.append("%s/../../lab3" % os.getcwd())

from db_generator import choose_variant_from_dict, get_input_int
import generator as m_gnr
import statistic as m_stat
import intializer as m_init

import psycopg2
import json

days_passed = 0
game_started = 0
min_days_passed = 0
max_days_passed = 0


def pretty_print(phrase):
    print("\n-------------- %s ---------\n" % phrase)


def parse_game_condition(path):
    global days_passed, game_started, min_days_passed, max_days_passed

    params_dict = json.load(open(path, 'r'))
    days_passed = params_dict.__getitem__("days_passed")
    game_started = params_dict.__getitem__("game_started")
    min_days_passed = params_dict.__getitem__("min_days_passed")
    max_days_passed = params_dict.__getitem__("max_days_passed")
    pass


def store_game_condition(path):
    params_dict = {'days_passed': days_passed,
                   'game_started': game_started,
                   'min_days_passed': min_days_passed,
                   'max_days_passed': max_days_passed}
    with open(path, "w") as fp:
        json.dump(params_dict, fp)


def try_commit(conn):
    commit_allowed = choose_variant_from_dict(title="COMMIT CHANGES?", variants={0: 'no', 1: 'yes'})
    if commit_allowed:
        conn.commit()


# ----------------------- main ----------------------------------
if __name__ == '__main__':

    pretty_print("damned_capitalism launched")

    # --------------------------- initializing --------------------------------------
    pretty_print("initializing")
    parse_game_condition("../cfg/world_cfg.json")
    m_gnr.init_generator_params_from_json("../cfg/generator_cfg.json")

    login = "manager"
    password = '1234'

    conn = psycopg2.connect(dbname='damned_capitalism', user=login, password=password, host='localhost')
    cursor = conn.cursor()

    if not game_started:
        game_started = 1
        m_gnr.generate_new_game(cursor=cursor)
        conn.commit()

    # ------------------------------- filling -----------------------------------------
    fill_complete = False
    while not fill_complete:

        # --------------------------- configurating --------------------------------------
        ti = choose_variant_from_dict(
            "AVAILABLE ACTIONS:",
            {0: 'new game', 1: 'add data manually', 2: 'pass days', 3: 'check statistic', 9: 'exit'}
        )

        # ------------------------ new game --------------------------------------
        if ti == 0:
            new_game = choose_variant_from_dict("ARE YOU SURE?", variants={0: 'no', 1: 'yes'})
            if new_game:
                days_passed = 0
                m_gnr.generate_new_game(cursor=cursor)
                try_commit(conn)


        # ------------------------ add data manually --------------------------------------
        elif ti == 1:
            m_gnr.generate_manually(cursor=cursor)

        # ------------------------ pass days  --------------------------------------
        elif ti == 2:
            days_passed += get_input_int("How many days will pass?(%d - %d)" %
                                         (min_days_passed, max_days_passed),
                                         min=min_days_passed, max=max_days_passed)


        # ------------------------ check statistic --------------------------------------
        elif ti == 3:
            m_stat.get_stat()

        # ------------------------ exiting --------------------------------------
        elif ti == 9:
            pretty_print("exiting")
            fill_complete = True

    store_game_condition("../cfg/world_cfg.json")
    cursor.close()
    conn.close()
