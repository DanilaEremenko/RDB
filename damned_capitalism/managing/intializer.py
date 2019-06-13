import json


def init_tables(cursor):

    params_dict = json.load(open("../res/markets.json", 'r'))
    print(params_dict)