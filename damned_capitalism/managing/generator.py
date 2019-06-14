from db_generator import *
import json


# ------------------------ parameters for generation -----------------------------------
MIN_PRICE = 0
MAX_PRICE = 0

MIN_VALUE = 0
MAX_VALUE = 0

MIN_WEIGHT = 0
MAX_WEIGHT = 0

MAX_VCH_LEN = 0
ITEM_AMOUNT = 0


# ------------------------------ PARSING METHODS ----------------------------
def init_generator_params_from_json(path):
    """
    Load params from json file by path. Json file must contain dictionary.
    :param path:
    :return:
    """
    print("PARSING PARAMS FROM FILE %s... " % path, end="")

    params_dict = json.load(open(path, 'r'))

    global MIN_PRICE, MAX_PRICE, \
        MIN_VALUE, MAX_VALUE, \
        MIN_WEIGHT, MAX_WEIGHT, \
        MAX_VCH_LEN, ITEM_AMOUNT

    MIN_PRICE = params_dict.__getitem__('MIN_PRICE')
    MAX_PRICE = params_dict.__getitem__('MAX_PRICE')

    MIN_VALUE = params_dict.__getitem__('MIN_VALUE')
    MAX_VALUE = params_dict.__getitem__('MAX_VALUE')

    MIN_WEIGHT = params_dict.__getitem__('MIN_WEIGHT')
    MAX_WEIGHT = params_dict.__getitem__('MAX_WEIGHT')

    MAX_VCH_LEN = params_dict.__getitem__('MAX_VCH_LEN')
    ITEM_AMOUNT = params_dict.__getitem__('ITEM_AMOUNT')

    print("ok")

    pass


def init_table_with_json(cursor, tab_name, json_path):
    jdict = json.load(open(json_path, 'r'))
    for id, atr_turp in jdict.items():
        req = "insert into %s values (%s, " % (tab_name, id)

        for atr in atr_turp:
            req += "\'%s\'," % atr

        req = req[:req.__len__() - 1] + ");"
        # print(req)
        cursor.execute(req)


def generate_new_game(cursor):
    # -------------------- clean tables ---------------------------------
    for tab_name in ('person_item', 'item', 'person'):
        cursor.execute("delete from %s * cascade;" % tab_name)

    # --------------- generate items ----------------------
    add_into_table(
        cursor, table_name="item",
        fields={'id': PID, 'name': PSEQ, 'price': PINT, 'value': PINT},

        bounds=[(2, 3), (MIN_PRICE, MAX_PRICE), (MIN_VALUE, MAX_VALUE)],

        lines_amount=ITEM_AMOUNT
    )
