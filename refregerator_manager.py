import psycopg2
import numpy as np
from random_word import RandomWords


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


def choose_variant_from_dict(title, variants):
    variants_str = ""
    for n, name in variants.items(): variants_str += "%d:%s\n" % (n, name)

    while True:
        answ = get_input_int(title="CHOOSE %s\n%s" % (title, variants_str))

        if variants.keys().__contains__(answ):
            return answ
        else:
            print("Unexpected value!\n")


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


def add_into_refregerator(cursor):
    way = choose_variant_from_dict("WAY OF ADDING", {1: 'random', 2: 'not random'})

    if way == 1:
        min = 1
        max = 50
        num = get_input_int(title="HOW MANY?[%d - %d]" % (min, max), min=min, max=max)

        # id in refregerator
        cursor.execute("select count(id) from refregerator;")
        rid = cursor.fetchall()[0][0]

        # product_id bounds
        prmin_id = 1
        cursor.execute("select count(id) from product;")
        prmax_id = cursor.fetchall()[0][0]

        # market_name_id bounds
        markmin_id = 1
        cursor.execute("select count(id) from market_name;")
        markmax_id = cursor.fetchall()[0][0]

        for i in range(0, num):
            rid += 1
            product_id = np.random.randint(prmin_id, prmax_id + 1)
            markname_id = np.random.randint(markmin_id, markmax_id + 1)
            price = np.random.randint(20, 400)
            disc_price = np.random.randint(1, 100)
            day_before_expiring = np.random.randint(14, 700)
            amount = np.random.randint(1, 5)

            cursor.execute("insert into refregerator values(%d,%d,%d,%d,%d,%s,%d,%d);" %
                           (rid, product_id, markname_id, price, disc_price, "current_date", day_before_expiring,
                            amount))

            print("insert into refregerator values (%d,%d,%d,%d,%d,%s,%d,%d);" %
                  (rid, product_id, markname_id, price, disc_price, "current_date", day_before_expiring,
                   amount))



    elif way == 2:
        print("not random still isn't working")  # TODO
    else:
        raise ValueError("excuse me what the fuck")

    pass


def add_into_product():
    cursor.execute("select count(id) from product;")
    prid = cursor.fetchall()[0][0]

    name = get_input_str(title="input name of product:")

    mark = get_input_str(title="input mark name:")

    priority = choose_variant_from_dict(title="CHOOSE PRIORITY:", variants={0: 'low', 1: 'normal', 2: 'high'})

    cursor.execute("select * from cook_condition;")
    cook_cond_id = choose_variant_from_turp(title="CHOOSE COOK CONDITION", variants=cursor.fetchall())

    cursor.execute("select * from product_type;")
    pr_type = choose_variant_from_turp(title="CHOOSE PRODUCT TYPE", variants=cursor.fetchall())

    cursor.execute("insert into product values(%d,%s,%s,%d,%d,%d);" %
                   (prid, name, mark, priority, cook_cond_id, pr_type))

    print("insert into product values(%d,%s,%s,%d,%d,%d);" %
          (prid, name, mark, priority, cook_cond_id, pr_type))


if __name__ == '__main__':
    login = "refregerator_manager"
    password = input("Input password for role \'%s\'" % login)
    conn = psycopg2.connect(dbname='refregerator', user=login, password=password, host='localhost')
    cursor = conn.cursor()

    fill_complete = False
    while not fill_complete:

        print("-------------------------------")
        ti = choose_variant_from_dict("TABLE", {1: 'refregerator', 2: 'product', 3: 'exit'})

        if ti == 1:
            add_into_refregerator(cursor)
        elif ti == 2:
            add_into_product()
        elif ti == 3:
            fill_complete = True

    commit_allowed = choose_variant_from_dict(title="COMMIT CHANGES?", variants={0: 'no', 1: 'yes'})
    if commit_allowed:
        conn.commit()
    cursor.close()
    conn.close()

# select table_name from information_schema.tables;
# cursor.execute('SELECT * FROM refregerator')
# records = cursor.fetchall()
