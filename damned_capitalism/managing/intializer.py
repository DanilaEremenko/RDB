import json


def init_tables(cursor):
    for market_name in json.load(open("../res/markets.json", 'r')).values():
        print(market_name)
        cursor.execute("insert into table market values (default , %s, 0);" % market_name)

    for food_type in json.load(open("../res/markets.json", 'r')).values():
        cursor.execute("insert into table food_type values (default , %s);" % food_type)
