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
        answ = get_input_int(title="CHOOSE %s\n%s" % (title, variants_str))

        if variants.keys().__contains__(answ):
            return answ
        else:
            print("Unexpected value!\n")


# ------------------------------------------------------------------------------------------
def get_table_turp(table_name):
    min = 0
    cursor.execute("select * from %s;" % table_name)
    table = cursor.fetchall()
    max = table.__len__()
    return (min, max, table)


# ------------------------------------------------------------------------------------------
def choose_variant_from_turp(title, variants):
    variants_str = ""
    for n, name in variants: variants_str += "%d:%s\n" % (n, name)

    while True:
        answ = get_input_int(title="CHOOSE %s\n%s" % (title, variants_str))

        for var in variants:
            if var.__contains__(answ):
                return answ
            else:
                print("Unexpected value!\n")


# ------------------------------------------------------------------------------------------
def add_into_refregerator(cursor, min=1, max=2000):
    way = choose_variant_from_dict("WAY OF ADDING", {1: 'random', 2: 'not random'})

    if way == 1:
        num = get_input_int(title="HOW MANY?[%d - %d]" % (min, max), min=min, max=max)

        for i in range(0, num):
            # id in refregerator
            cursor.execute("select count(id) from refregerator;")
            rid = cursor.fetchall()[0][0] + 1

            # product_id bounds
            (prmin_id, prmax_id, products) = get_table_turp("product")
            idp = np.random.randint(low=prmin_id, high=prmax_id)
            product_id = products[idp][0]

            # market_name_id bounds
            (markmin_id, markmax_id, markets) = get_table_turp("market_name")
            idp = np.random.randint(low=markmin_id, high=markmax_id)
            markname_id = markets[idp][0]

            price = np.random.randint(MIN_PRICE, MAX_PRICE)
            disc_price = np.random.randint(MIN_DPRICE, MAX_DPRICE)
            day_before_expiring = np.random.randint(MIN_DAY_EXP, MAX_DAY_EXP)
            amount = np.random.randint(MIN_AM, MAX_AM)

            cursor.execute("insert into refregerator values(%d,%d,%d,%d,%d,%s,%d,%d);" %
                           (rid, product_id, markname_id, price, disc_price, "current_date", day_before_expiring,
                            amount))

            print("insert into refregerator values (%d,%d,%d,%d,%d,\'%s\',%d,%d);" %
                  (rid, product_id, markname_id, price, disc_price, "current_date", day_before_expiring,
                   amount))



    elif way == 2:
        print("not random still isn't working")  # TODO
    pass


# ------------------------------------------------------------------------------------------
def add_into_product(cursor, rw, min=1, max=2000):
    way = choose_variant_from_dict("WAY OF ADDING", {1: 'random', 2: 'not random'})

    # random
    if way == 1:
        num = get_input_int(title="HOW MANY?[%d - %d]" % (min, max), min=min, max=max)

        for i in range(0, num):
            # next id
            cursor.execute("select max(id) from product;")
            prid = cursor.fetchall()[0][0] + 1

            name = rw.random_word()
            while name.__len__() > VCH_MAX_LEN:
                name = rw.random_word()

            mark = rw.random_word()
            while mark.__len__() > VCH_MAX_LEN:
                mark = rw.random_word()

            priority = np.random.randint(low=MIN_PRIOR, high=MAX_PRIOR + 1)

            # cook conditions info
            (ccond_min_id, ccond_max_id, cook_conds) = get_table_turp("cook_condition")
            idp = np.random.randint(low=ccond_min_id, high=ccond_max_id)
            cook_cond_id = cook_conds[idp][0]

            # product types info
            (prtype_min_id, prtype_max_id, prtypes) = get_table_turp("product_type")
            idp = np.random.randint(low=prtype_min_id, high=prtype_max_id)
            pr_type = prtypes[idp][0]

            print("insert into product values(%d,\'%s\',\'%s\',%d,%d,%d);" %
                  (prid, name, mark, priority, cook_cond_id, pr_type))

            cursor.execute("insert into product values(%d,\'%s\',\'%s\',%d,%d,%d);" %
                           (prid, name, mark, priority, cook_cond_id, pr_type))




    # not random
    elif way == 2:
        cursor.execute("select max(id) from product;")
        prid = cursor.fetchall()[0][0] + 1

        name = get_input_str(title="input name of product:")

        mark = get_input_str(title="input mark name:")

        priority = choose_variant_from_dict(title="CHOOSE PRIORITY:", variants={0: 'low', 1: 'normal', 2: 'high'})

        cursor.execute("select * from cook_condition;")
        cook_cond_id = choose_variant_from_turp(title="CHOOSE COOK CONDITION", variants=cursor.fetchall())

        cursor.execute("select * from product_type;")
        pr_type = choose_variant_from_turp(title="CHOOSE PRODUCT TYPE", variants=cursor.fetchall())

        print("insert into product values(%d,\'%s\',\'%s\',%d,%d,%d);" %
              (prid, name, mark, priority, cook_cond_id, pr_type))

        cursor.execute("insert into product values(%d,\'%s\',\'%s\',%d,%d,%d);" %
                       (prid, name, mark, priority, cook_cond_id, pr_type))
    pass


# ------------------------------------------------------------------------------------------
def add_into_product_type(cursor, rw, min=1, max=2000):
    # TODO
    pass


# ------------------------------------------------------------------------------------------
def add_into_market_name(cursor, rw, min, max=2000):
    # TODO
    pass


# ------------------------------------------------------------------------------------------
def parse_params_from_cf(path):
    # TODO
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
        ti = choose_variant_from_dict("TABLE", {1: 'refregerator', 2: 'product', 3: 'exit'})

        if ti == 1:
            add_into_refregerator(cursor)
        elif ti == 2:
            add_into_product(cursor, rw)
        elif ti == 3:
            fill_complete = True

    commit_allowed = choose_variant_from_dict(title="COMMIT CHANGES?", variants={0: 'no', 1: 'yes'})
    if commit_allowed:
        conn.commit()
    cursor.close()
    conn.close()
