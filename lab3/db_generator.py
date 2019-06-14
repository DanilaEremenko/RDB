from random_words import RandomWords, RandomNicknames
import numpy as np

# ----------------------------- types of fields ----------------------------------
PINT = 0  # param is integer
PSTR = 1  # param is word
PSEQ = 2  # param is sequence of words
PREF = 3  # param is reference
PDATE = 4  # param is date
PID = 5  # param is id
PNAME = 6  # param is name


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
        answ = get_input_int(title="-------- %s ----------\n%s" % (title, variants_str))

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
def get_table_turp(cursor, table_name):
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


def get_random_name(rn, min_size, max_size):
    name = rn.random_nick()
    while name.__len__() < min_size or name.__len__() > max_size:
        name = rn.random_nick()
    return name


# ------------------------------ MAIN METHOD FOR TABLES FILLING---------------------------
def add_into_table(cursor, table_name, fields, min_av=None, max_av=None, bounds=None, lines_amount=None, verbose=False):
    """
    :param cursor: cursor to database
    :param table_name: name of fielded table
    :param fields: dictionary that contains fields in keys and types in values
    :param bounds: bounds for int fields
    :param min_av: min amount of randomized lines
    :param max_av: max amount of randomized lines
    :return: pass
    """
    rw = RandomWords()
    rn = RandomNicknames()

    if lines_amount == None:
        if min_av == None or max_av == None: raise Exception("nor lines_amount or min_av & max_av passed")
        lines_amount = get_input_int(title="HOW MANY?[%d - %d]" % (min_av, max_av), min=min_av, max=max_av)

    print("generate %d lines for table %s..." % (lines_amount, table_name))
    for i in range(0, lines_amount):

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
                    seq += get_random_word(rw, min_size=1, max_size=20) + " "
                request += "\'%s\'," % seq[:seq.__len__() - 1]
                bi += 1

            elif partype == PREF:
                (min_id, max_id, lines) = get_table_turp(cursor, field)
                if min_id == 0 and max_id == 0:
                    raise Exception("table = %s is empty" % field)
                currid = np.random.randint(low=min_id, high=max_id)
                request += "%d," % lines[currid][0]

            elif partype == PDATE:
                request += "%s," % "current_date"

            elif partype == PID:
                rid = get_free_id(cursor, table_name)
                request += "%d," % rid

            elif partype == PNAME:
                MIN_B = bounds[bi][0]
                MAX_B = bounds[bi][1]
                name = get_random_name(rn, min_size=MIN_B, max_size=MAX_B)
                request += "\'%s\'," % name
                bi += 1

        request = request[:request.__len__() - 1] + ")"

        if verbose: print(request)
        cursor.execute(request)

    pass


# ------------------------------ run sql file --------------------------------
def run_sql(cursor, addr):
    sql_file = open(addr, 'r')
    sql_code = ""
    for line in sql_file.readlines(): sql_code += line
    cursor.execute(sql_code)
