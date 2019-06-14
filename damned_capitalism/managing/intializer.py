import json


def init_tables(cursor):
    for market_name in json.load(open("../res/markets.json", 'r')).values():
        cursor.execute("insert into market values (default , '%s', 0);" % market_name)

    for food_type in json.load(open("../res/markets.json", 'r')).values():
        cursor.execute("insert into food_type values (default , '%s');" % food_type)
