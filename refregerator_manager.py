import psycopg2
import numpy as np
from random_words import RandomWords

VCH_MAX_LEN = 15

MIN_PRIOR = 0
MAX_PRIOR = 2

MIN_PRICE = 20
MAX_PRICE = 400

MIN_DPRICE = 10
MAX_DPRICE = 100

MIN_DAY_EXP = 10
MAX_DAY_EXP = 700

MIN_AM = 1
MAX_AM = 5

# types of fields
PINT = 0
PSTR = 1
PREF = 2
PDATE = 3
PID = 4


# ------------------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------------------
def choose_variant_from_dict(title, variants):
    variants_str = ""
    for n, name in variants.items(): variants_str += "%d:%s\n" % (n, name)

    while True:
        answ = get_input_int(title="%s\n%s" % (title, variants_str))

        if variants.keys().__contains__(answ):
            return answ
        else:
            print("Unexpected value!\n")


# ------------------------------------------------------------------------------------------
def get_table_turp(table_name):
    cursor.execute("select * from %s;" % table_name)
    table = cursor.fetchall()
    min_id = 0
    max_id = table.__len__()
    return (min_id, max_id, table)


# ------------------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------------------
def add_into_table(cursor, rw, table_name, fields, bounds=None, min=1, max=2000):
    """
    :param cursor: cursor to database
    :param rw: random word
    :param table_name: name of fielded table
    :param fields: dictionary that contains fields in keys and types in values
    :param bounds: bounds for int fields
    :param min: min amount of randomized lines
    :param max: max amount of randomized lines
    :return: pass
    """
    way = choose_variant_from_dict("CHOOSE WAY OF ADDING FOR TABLE \'%s\'" % table_name, {1: 'random', 2: 'not random'})

    if way == 1:
        num = get_input_int(title="HOW MANY?[%d - %d]" % (min, max), min=min, max=max)

        for i in range(0, num):

            request = "insert into %s values(" % table_name

            bi = 0
            for field, partype in fields.items():
                if partype == PINT:
                    MIN_B = bounds[bi][0]
                    MAX_B = bounds[bi][1]
                    request += "%d," % np.random.randint(MIN_B, MAX_B)
                    bi += 1

                elif partype == PSTR:  # TODO add bounds control
                    word = rw.random_word()
                    while word.__len__() > VCH_MAX_LEN:
                        word = rw.random_word()
                    request += "\'%s\'," % word

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


# ------------------------------------------------------------------------------------------
def parse_params_from_cf(path):
    # TODO add
    pass


# ------------------------------------------------------------------------------------------
if __name__ == '__main__':

    login = "refregerator_manager"
    password = input("Input password for role \'%s\'" % login)

    conn = psycopg2.connect(dbname='refregerator', user=login, password=password, host='localhost')
    cursor = conn.cursor()
    rw = RandomWords()

    fill_complete = False
    while not fill_complete:

        print("-------------------------------")
        # define tables, which will be filled
        ti = choose_variant_from_dict(
            "CHOOSE TABLE",
            {1: 'refregerator', 2: 'product', 3: 'exit'}
        )

        # ------------------- change tables : refregerator -------------------------------------
        if ti == 1:
            add_into_table(
                cursor, rw, table_name="refregerator",
                fields={'id': PID, 'product': PREF, 'market_name': PREF, 'price': PINT, 'disc_price': PINT,
                        'buying_date': PDATE,
                        'day_before_expiring': PINT, 'amount': PINT},
                bounds=[(MIN_PRICE, MAX_PRICE), (MIN_DPRICE, MAX_DPRICE), (MIN_DAY_EXP, MAX_DAY_EXP), (MIN_AM, MAX_AM)],
            )


        # --------------- change tables : product & way_of cooking product ----------------------
        elif ti == 2:
            add_into_table(
                cursor, rw, table_name="product",
                fields={'id': PID, 'name': PSTR, 'mark': PSTR, 'priority': PINT, 'cook_condition': PREF,
                        'product_type': PREF},
                bounds=[(MIN_PRIOR, MAX_PRIOR)]
            )

            # -------------------- fill way_of_cooking_product --------------------------------------------
            # add >=1 refererence to way_of_cooking_product for every product with condition 'not ready'
            (min_wid, max_wid, lines) = get_table_turp('way_of_cooking')

            # calculate request id
            rid = get_free_id(cursor, "way_of_cooking_product")

            # select only ids of 'not ready'
            cursor.execute("select id from product where cook_condition_id = 2;")

            for prod_id in np.array(cursor.fetchall()):
                way_id = np.random.randint(min_wid+1,max_wid+1)
                print("insert into way_of_cooking_product values (%d, %d, %d)" % (rid, prod_id, way_id))
                cursor.execute(
                    "insert into way_of_cooking_product values (%d, %d, %d)" % (rid, prod_id, way_id))
                rid += 1




        # ------------------------------ exit from program ------------------------------
        elif ti == 3:
            fill_complete = True

    # -------------------------- commit or not commit changes ---------------------------
    commit_allowed = choose_variant_from_dict(title="COMMIT CHANGES?", variants={0: 'no', 1: 'yes'})
    if commit_allowed:
        conn.commit()
    cursor.close()
    conn.close()
