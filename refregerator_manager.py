import psycopg2
import numpy as np


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


def choose_variant(title, variants):
    variants_str = ""
    for n, name in variants.items(): variants_str += "%d:%s\n" % (n, name)

    while True:
        answ = get_input_int(title="CHOOSE %s\n%s" % (title, variants_str))

        if variants.keys().__contains__(answ):
            return answ
        else:
            print("Unexpected value!\n")


def add_into_refregerator(cursor):
    way = choose_variant("WAY OF ADDING", {1: 'random', 2: 'not random'})

    if way == 1:
        min = 1
        max = 50
        num = get_input_int(title="HOW MANY?[%d - %d]" % (min, max), min=min, max=max)

        cursor.execute("select count(id) from product;")
        min_id = 1
        max_id = cursor.fetchall()[0][0]

        for i in range(0, num):
            product_id = np.random.randint(min_id, max_id + 1)
            print("product_id = %d" % product_id)
            continue  # TODO


    elif way == 2:
        print("not random still isn't working")  # TODO
    else:
        raise ValueError("excuse me what the fuck")

    pass


def add_into_product():
    pass


if __name__ == '__main__':
    conn = psycopg2.connect(dbname='refregerator', user='postgres', host='localhost')
    cursor = conn.cursor()

    fill_complete = False
    while not fill_complete:

        print("-------------------------------")
        ti = choose_variant("TABLE", {1: 'refregerator', 2: 'product', 3: 'exit'})

        if ti == 1:
            add_into_refregerator(cursor)
        elif ti == 2:
            add_into_product()
        elif ti == 3:
            fill_complete = True

    cursor.close()
    conn.close()
# select table_name from information_schema.tables;
# cursor.execute('SELECT * FROM refregerator')
# records = cursor.fetchall()
