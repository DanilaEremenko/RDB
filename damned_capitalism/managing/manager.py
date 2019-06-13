import sys
import os

sys.path.append("%s/../../lab3" % os.getcwd())

from db_generator import choose_variant_from_dict
import generator as m_gnr
import statistic as m_stat
import intializer as m_init

import psycopg2


def pretty_print(phrase):
    print("\n-------------- %s ---------\n" % phrase)


if __name__ == '__main__':

    pretty_print("damned_capitalism launched")

    # --------------------------- initializing --------------------------------------
    pretty_print("initializing")
    m_gnr.init_generator_params_from_json("../cfg/generator_cfg.json")

    login = "manager"
    password = '1234'

    conn = psycopg2.connect(dbname='damned_capitalism', user=login, password=password, host='localhost')
    cursor = conn.cursor()

    m_init.init_tables(cursor)

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
                # TODO
                m_gnr.generate(cursor=cursor)
                commit_allowed = choose_variant_from_dict(title="COMMIT CHANGES?", variants={0: 'no', 1: 'yes'})
                if commit_allowed:
                    conn.commit()
                cursor.close()
                conn.close()
            else:
                continue


        # ------------------------ add data manually --------------------------------------
        elif ti == 1:
            print("not available")

        # ------------------------ pass days  --------------------------------------
        elif ti == 2:
            print("not available")

        # ------------------------ check statistic --------------------------------------
        elif ti == 3:
            m_stat.get_stat()

        # ------------------------ exiting --------------------------------------
        elif ti == 9:
            pretty_print("exiting")
            fill_complete = True

    cursor.close()
    conn.close()
