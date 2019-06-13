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
def store_json(path):
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


def parse_json(path):
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
def generate(cursor):
    fill_complete = False
    while not fill_complete:

        print("-------------------------------")
        # define tables, which will be filled
        ti = choose_variant_from_dict(
            "CHOOSE TABLE",
            {0: 'client', 1: 'refregerator', 2: 'product', 3: 'recipe', 4: 'recipe_product', 5: 'exit'}
        )

        # ------------------- change table : refregerator -------------------------------------
        if ti == 0:
            add_into_table(
                cursor, table_name="client",
                fields={'id': PID, 'first_name': PNAME, 'second_name': PNAME, 'account': PINT},
                bounds=[(1, MAX_VCH_LEN), (1, MAX_VCH_LEN), (MIN_ACCOUNT, MAX_ACCOUNT)],
                min_av=MIN_ADD_AVAIL,
                max_av=MAX_ADD_AVAIL
            )

        # ------------------- change table : refregerator -------------------------------------
        if ti == 1:
            add_into_table(
                cursor, table_name="refregerator",
                fields={'id': PID, 'product': PREF, 'market_name': PREF, 'price': PINT, 'disc_price': PINT,
                        'buying_date': PDATE,
                        'day_before_expiring': PINT, 'amount': PINT},
                bounds=[(MIN_PRICE, MAX_PRICE), (MIN_DPRICE, MAX_DPRICE), (MIN_DAY_EXP, MAX_DAY_EXP), (MIN_AM, MAX_AM)],
                min_av=MIN_ADD_AVAIL,
                max_av=MAX_ADD_AVAIL
            )

        # --------------- change tables : product & way_of cooking product ----------------------
        elif ti == 2:
            add_into_table(
                cursor, table_name="product",
                fields={'id': PID, 'name': PSTR, 'mark': PSTR, 'priority': PINT, 'cook_condition': PREF,
                        'product_type': PREF},
                bounds=[(1, MAX_VCH_LEN), (1, MAX_VCH_LEN), (MIN_PRIOR, MAX_PRIOR)],
                min_av=MIN_ADD_AVAIL,
                max_av=MAX_ADD_AVAIL
            )

        # --------------- change table : recipe ----------------------
        elif ti == 3:
            add_into_table(
                cursor, table_name="recipe",
                fields={'id': PID, 'name': PSEQ, 'weight': PINT, 'way_of_cooking': PREF},
                bounds=[(2, 3), (MIN_WEIGHT, MAX_WEIGHT)],
                min_av=MIN_ADD_AVAIL,
                max_av=MAX_ADD_AVAIL
            )

        # --------------- change table : recipe_product ---------------
        elif ti == 4:
            add_into_table(
                cursor, table_name="recipe_product",
                fields={'id': PID, 'recipe': PREF, 'product': PREF, 'product_amount': PINT},
                bounds=[(MIN_AM, MAX_AM)],
                min_av=MIN_ADD_AVAIL,
                max_av=MAX_ADD_AVAIL
            )

        # ------------------------------ exit from program ------------------------------
        elif ti == 5:
            fill_complete = True

