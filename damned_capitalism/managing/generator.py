from db_generator import *
import json

# ------------------------ parameters for generation -----------------------------------
MAX_VCH_LEN = 0

MIN_PRIOR = 0
MAX_PRIOR = 0

MIN_PRICE = 0
MAX_PRICE = 0

MIN_DPRICE = 0
MAX_DPRICE = 0

MIN_DAY_EXP = 0
MAX_DAY_EXP = 0

MIN_AM = 0
MAX_AM = 0

MIN_WEIGHT = 0
MAX_WEIGHT = 0

MIN_ACCOUNT = 0
MAX_ACCOUNT = 0

MIN_ADD_AVAIL = 0
MAX_ADD_AVAIL = 0


# ------------------------------ PARSING METHODS ----------------------------
def store_generator_params_to_json(path):
    """
    Store dictionary with params to the file by the path.
    :param path:
    :return:
    """
    params_dict = {'MAX_VCH_LEN': 15,
                   'MIN_PRIOR': 0,
                   'MAX_PRIOR': 2,

                   'MIN_PRICE': 20,
                   'MAX_PRICE': 400,

                   'MIN_DPRICE': 10,
                   'MAX_DPRICE': 100,

                   'MIN_DAY_EXP': 10,
                   'MAX_DAY_EXP': 700,

                   'MIN_AM': 1,
                   'MAX_AM': 5,

                   'MIN_ACCOUNT': 20_000,
                   'MAX_ACCOUNT': 60_000,

                   'MIN_ADD_AVAIL': 1,
                   'MAX_ADD_AVAIL': 2000
                   }
    with open(path, "w") as fp:
        json.dump(params_dict, fp)

    pass


def init_generator_params_from_json(path):
    """
    Load params from json file by path. Json file must contain dictionary.
    :param path:
    :return:
    """
    print("PARSING PARAMS FROM FILE %s... " % path, end="")

    params_dict = json.load(open(path, 'r'))

    global MAX_VCH_LEN, MIN_PRIOR, MAX_PRIOR, \
        MIN_PRICE, MAX_PRICE, \
        MIN_DPRICE, MAX_DPRICE, \
        MIN_DAY_EXP, MAX_DAY_EXP, \
        MIN_AM, MAX_AM, \
        MIN_WEIGHT, MAX_WEIGHT, \
        MIN_ACCOUNT, MAX_ACCOUNT, \
        MIN_ADD_AVAIL, MAX_ADD_AVAIL

    MAX_VCH_LEN = params_dict.__getitem__('MAX_VCH_LEN')

    MIN_PRIOR = params_dict.__getitem__('MIN_PRIOR')
    MAX_PRIOR = params_dict.__getitem__('MAX_PRIOR')

    MIN_PRICE = params_dict.__getitem__('MIN_PRICE')
    MAX_PRICE = params_dict.__getitem__('MAX_PRICE')

    MIN_DPRICE = params_dict.__getitem__('MIN_DPRICE')
    MAX_DPRICE = params_dict.__getitem__('MAX_DPRICE')

    MIN_DAY_EXP = params_dict.__getitem__('MIN_DAY_EXP')
    MAX_DAY_EXP = params_dict.__getitem__('MAX_DAY_EXP')

    MIN_AM = params_dict.__getitem__('MIN_AM')
    MAX_AM = params_dict.__getitem__('MAX_AM')

    MIN_WEIGHT = params_dict.__getitem__('MIN_WEIGHT')
    MAX_WEIGHT = params_dict.__getitem__('MAX_WEIGHT')

    MIN_ACCOUNT = params_dict.__getitem__('MIN_ACCOUNT')
    MAX_ACCOUNT = params_dict.__getitem__('MAX_ACCOUNT')

    MIN_ADD_AVAIL = params_dict.__getitem__('MIN_ADD_AVAIL')
    MAX_ADD_AVAIL = params_dict.__getitem__('MAX_ADD_AVAIL')

    print("ok")

    pass


# ------------------------------------------------------------------------------------------
def generate_manually(cursor):
    fill_complete = False
    while not fill_complete:

        print("-------------------------------")
        # define tables, which will be filled
        ti = choose_variant_from_dict(
            "CHOOSE TABLE",
            {0: 'client_refrigerator', 1: 'market_refrigerator', 2: 'food', 3: 'exit'}
        )

        # ------------------- change table : client_refrigerator -------------------------------------
        if ti == 0:
            add_into_table \
                    (
                    cursor, table_name="client_refrigerator",
                    fields={'id': PID, 'client': PREF, 'food': PREF, 'market': PREF,
                            'price': PINT, 'disc_price': PINT, 'buying_date': PDATE,
                            'day_before_expiring': PINT, 'amount': PINT},

                    bounds=[(MIN_PRICE, MAX_PRICE), (MIN_DPRICE, MAX_DPRICE), (MIN_DAY_EXP, MAX_DAY_EXP),
                            (MIN_AM, MAX_AM)],

                    min_av=MIN_ADD_AVAIL,
                    max_av=MAX_ADD_AVAIL
                )

        # --------------- change table : market_refrigerator ----------------------
        elif ti == 1:
            add_into_table(
                cursor, table_name="market_refrigerator",
                fields={'id': PID, 'market': PREF, 'food': PREF,
                        'price': PINT, 'disc_price': PINT,
                        'day_before_expiring': PINT, 'amount': PINT},

                bounds=[(MIN_PRICE, MAX_PRICE), (MIN_DPRICE, MAX_DPRICE), (MIN_DAY_EXP, MAX_DAY_EXP),
                        (MIN_AM, MAX_AM)],

                min_av=MIN_ADD_AVAIL,
                max_av=MAX_ADD_AVAIL
            )

        # --------------- change table : food ----------------------
        elif ti == 2:
            add_into_table(
                cursor, table_name="recipe",
                fields={'id': PID, 'name': PSEQ, 'food_type': PREF},

                bounds=[(2, 3)],

                min_av=MIN_ADD_AVAIL,
                max_av=MAX_ADD_AVAIL
            )

        # ------------------------------ exit from program ------------------------------
        elif ti == 3:
            fill_complete = True


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
    for tab_name in ('market_refrigerator', 'client_refrigerator', 'client', 'market', 'food', 'food_type'):
        cursor.execute("delete from %s * cascade;" % tab_name)

    # -------------------- init tables from json -------------------------
    for tab_name in ('client', 'market', 'food_type'):
        init_table_with_json(cursor=cursor, tab_name=tab_name, json_path="../res/%ss.json" % tab_name)

    # --------------- change table : food ----------------------
    add_into_table(
        cursor, table_name="food",
        fields={'id': PID, 'name': PSEQ, 'food_type': PREF},

        bounds=[(2, 3)],

        min_av=MIN_ADD_AVAIL,
        max_av=MAX_ADD_AVAIL,
        lines_amount=2000
    )

    # --------------- change table : market_refrigerator ----------------------
    add_into_table(
        cursor, table_name="market_refrigerator",
        fields={'id': PID, 'market': PREF, 'food': PREF,
                'price': PINT, 'disc_price': PINT,
                'day_before_expiring': PINT, 'amount': PINT},

        bounds=[(MIN_PRICE, MAX_PRICE), (MIN_DPRICE, MAX_DPRICE), (MIN_DAY_EXP, MAX_DAY_EXP),
                (MIN_AM, MAX_AM)],

        min_av=MIN_ADD_AVAIL,
        max_av=MAX_ADD_AVAIL,
        lines_amount=2000
    )
