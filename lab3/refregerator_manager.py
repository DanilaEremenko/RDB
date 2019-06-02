import psycopg2
import numpy as np
from random_words import RandomWords
import sys
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

MIN_ADD_AVAIL = 0
MAX_ADD_AVAIL = 0

# ----------------------------- types of fields ----------------------------------
PINT = 0  # param is integer
PSTR = 1  # param is word
PSEQ = 2  # param is sequence of words
PREF = 3  # param is reference
PDATE = 4  # param is date
PID = 5  # param is id


# ------------------------------- GETTERS FROM CONSOLE --------------------------------------------------
def get_input_int(title=None, min=None, max=None):
    while True:
        if title != None:
            print(title)
        res = input()
        if res.isdigit():
            res = int(res)

            if (min != None) and (max != None):
                if (res >= min and res <= max):
                    return res
                else:
                    print("%d isn't between [%d,%d]" % (res, min, max))
            else:
                return res

        else:
            print("%s not an integer\n" % res)


def get_input_str(title=None, min_size=1, max_size=15):
    while True:
        if title != None:
            print(title)
        res = input()
        if not res.isdigit():

            if (res.__len__() >= min_size and res.__len__() <= max_size):
                return res
            else:
                print("%s isn't between [%d,%d]" % (res, min_size, max_size))

        else:
            print("%s not an string\n" % res)


# ------------------------------- CHOOSE FROM CONSOLE --------------------------------------
def choose_variant_from_dict(title, variants):
    variants_str = ""
    for n, name in variants.items(): variants_str += "%d:%s\n" % (n, name)

    while True:
        answ = get_input_int(title="%s\n%s" % (title, variants_str))

        if variants.keys().__contains__(answ):
            return answ
        else:
            print("Unexpected value!\n")


def choose_variant_from_turp(title, variants):
    """
    Correct processing of illegal value works.
    :param title:
    :param variants:
    :return: one of allowed number
    """
    variants_str = ""
    for n, name in variants: variants_str += "%d:%s\n" % (n, name)

    while True:
        answ = get_input_int(title="%s\n%s" % (title, variants_str))

        for var in variants:
            if var.__contains__(answ):
                return answ
            else:
                print("Unexpected value!\n")


# -------------------------------- GETTERS ------------------------------------------------
def get_table_turp(table_name):
    cursor.execute("select * from %s;" % table_name)
    table = cursor.fetchall()
    min_id = 0
    max_id = table.__len__()
    return (min_id, max_id, table)


def get_free_ids(cursor, table_name):
    """
    :param cursor:
    :param table_name:
    :return: array of free ids in table
    """

    cursor.execute("select id from %s;" % table_name)
    ids = np.array(cursor.fetchall())
    shids = ids + 1
    fids = np.empty(0, dtype=int)
    for shid in shids:
        if not ids.__contains__(shid):
            fids = np.append(fids, shid)
    return fids


def get_free_id(cursor, table_name):
    """
    :param cursor:
    :param table_name:
    :return: array of free ids in table
    """
    cursor.execute("select max(id) from %s" % table_name)
    max = cursor.fetchall()[0][0]
    if max == None:
        return 1
    else:
        return max + 1


def get_random_word(rw, min_size, max_size):
    word = rw.random_word()
    while word.__len__() < min_size or word.__len__() > max_size:
        word = rw.random_word()
    return word


# ------------------------------ MAIN METHOD FOR TABLES FILLING---------------------------
def add_into_table(cursor, rw, table_name, fields, min_av, max_av, bounds=None):
    """
    :param cursor: cursor to database
    :param rw: random word
    :param table_name: name of fielded table
    :param fields: dictionary that contains fields in keys and types in values
    :param bounds: bounds for int fields
    :param min_av: min amount of randomized lines
    :param max_av: max amount of randomized lines
    :return: pass
    """
    way = choose_variant_from_dict("CHOOSE WAY OF ADDING FOR TABLE \'%s\'" % table_name, {1: 'random', 2: 'not random'})

    if way == 1:
        num = get_input_int(title="HOW MANY?[%d - %d]" % (min_av, max_av), min=min_av, max=max_av)

        for i in range(0, num):

            request = "insert into %s values(" % table_name

            bi = 0
            for field, partype in fields.items():
                if partype == PINT:
                    MIN_B = bounds[bi][0]
                    MAX_B = bounds[bi][1]
                    request += "%d," % np.random.randint(MIN_B, MAX_B)
                    bi += 1

                elif partype == PSTR:
                    MIN_B = bounds[bi][0]
                    MAX_B = bounds[bi][1]
                    word = get_random_word(rw, min_size=MIN_B, max_size=MAX_B)
                    request += "\'%s\'," % word
                    bi += 1

                elif partype == PSEQ:
                    MIN_B = bounds[bi][0]
                    MAX_B = bounds[bi][1]
                    seq = ""
                    for i in range(MIN_B):
                        seq += get_random_word(rw, min_size=1, max_size=MAX_VCH_LEN) + " "
                    request += "\'%s\'," % seq[:seq.__len__() - 1]
                    bi += 1

                elif partype == PREF:
                    (min_id, max_id, lines) = get_table_turp(field)
                    currid = np.random.randint(low=min_id, high=max_id)
                    request += "%d," % lines[currid][0]

                elif partype == PDATE:
                    request += "%s," % "current_date"

                elif partype == PID:
                    rid = get_free_id(cursor, table_name)
                    request += "%d," % rid

            request = request[:request.__len__() - 1] + ")"

            print(request)
            cursor.execute(request)




    elif way == 2:
        print("not random still isn't working")  # TODO add
    pass


# ------------------------------ run sql file --------------------------------
def run_sql(addr):
    sql_file = open(addr, 'r')
    sql_code = ""
    for line in sql_file.readlines(): sql_code += line
    cursor.execute(sql_code)


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

    MIN_ADD_AVAIL = params_dict.__getitem__('MIN_ADD_AVAIL')
    MAX_ADD_AVAIL = params_dict.__getitem__('MAX_ADD_AVAIL')

    print("ok")

    pass


# ------------------------------------------------------------------------------------------
if __name__ == '__main__':
    if sys.argv.__len__() != 2:
        raise ValueError("Illegal amount of arguments = %d "
                         "(path to json config file must be passed)" % sys.argv.__len__())

    print("-------------------------------")
    param_path = sys.argv[1]
    # store_json(param_path)
    parse_json(param_path)
    print("-------------------------------")

    login = "refregerator_manager"
    password = input("Input password for role \'%s\'" % login)
    print("-------------------------------")

    conn = psycopg2.connect(dbname='refregerator', user=login, password=password, host='localhost')
    cursor = conn.cursor()
    rw = RandomWords()

    fill_complete = False
    while not fill_complete:

        print("-------------------------------")
        # define tables, which will be filled
        ti = choose_variant_from_dict(
            "CHOOSE TABLE",
            {1: 'refregerator', 2: 'product', 3: 'recipe', 4: 'recipe_product', 5: 'exit'}
        )

        # ------------------- change table : refregerator -------------------------------------
        if ti == 1:
            add_into_table(
                cursor, rw, table_name="refregerator",
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
                cursor, rw, table_name="product",
                fields={'id': PID, 'name': PSTR, 'mark': PSTR, 'priority': PINT, 'cook_condition': PREF,
                        'product_type': PREF},
                bounds=[(1, MAX_VCH_LEN), (1, MAX_VCH_LEN), (MIN_PRIOR, MAX_PRIOR)],
                min_av=MIN_ADD_AVAIL,
                max_av=MAX_ADD_AVAIL
            )

        # --------------- change table : recipe ----------------------
        elif ti == 3:
            add_into_table(
                cursor, rw, table_name="recipe",
                fields={'id': PID, 'name': PSEQ, 'weight':PINT, 'way_of_cooking': PREF},
                bounds=[(2, 3),(MIN_WEIGHT, MAX_WEIGHT)],
                min_av=MIN_ADD_AVAIL,
                max_av=MAX_ADD_AVAIL
            )

        # --------------- change table : recipe_product ---------------
        elif ti == 4:
            add_into_table(
                cursor, rw, table_name="recipe_product",
                fields={'id': PID, 'recipe': PREF, 'product': PREF, 'product_amount' : PINT },
                bounds=[(MIN_AM, MAX_AM)],
                min_av=MIN_ADD_AVAIL,
                max_av=MAX_ADD_AVAIL
            )

        # ------------------------------ exit from program ------------------------------
        elif ti == 5:
            fill_complete = True

    # -------------------------- commit or not commit changes ---------------------------
    commit_allowed = choose_variant_from_dict(title="COMMIT CHANGES?", variants={0: 'no', 1: 'yes'})
    if commit_allowed:
        conn.commit()
    cursor.close()
    conn.close()
