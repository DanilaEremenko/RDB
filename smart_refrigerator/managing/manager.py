import sys
import os

sys.path.append("%s/../../lab3" % os.getcwd())

from db_generator import choose_variant_from_dict
from generator import generate, parse_json
from statistic import get_stat
import psycopg2


def pretty_print(phrase):
    print("\n--------------%s---------\n" % phrase)


if __name__ == '__main__':

    pretty_print("smart_refrigerator manager launched")

    # --------------------------- configurating --------------------------------------
    pretty_print("configurating")
    parse_json("../cfg/generator_cfg.json")
    login = "manager"
    password = '1234'

    conn = psycopg2.connect(dbname='smart_refrigerator', user=login, password=password, host='localhost')
    cursor = conn.cursor()

    fill_complete = False
    while not fill_complete:

        # --------------------------- configurating --------------------------------------
        ti = choose_variant_from_dict(
            "AVAILABLE ACTIONS:",
            {0: 'add data manually', 1: 'generate data', 2: 'check statistic', 9: 'exit'}
        )

        # ------------------------ manually adding --------------------------------------
        if ti == 0:
            print("adding mannual still unavailable")



        # ------------------------ generate data --------------------------------------
        elif ti == 1:
            generate(cursor=cursor)
            commit_allowed = choose_variant_from_dict(title="COMMIT CHANGES?", variants={0: 'no', 1: 'yes'})
            if commit_allowed:
                conn.commit()
            cursor.close()
            conn.close()

        # ------------------------ generate data --------------------------------------
        elif ti == 2:
            get_stat()

        # ------------------------ exiting --------------------------------------
        elif ti == 9:
            pretty_print("exiting")
            fill_complete = True

    cursor.close()
    conn.close()
