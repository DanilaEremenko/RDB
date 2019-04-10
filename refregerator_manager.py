import psycopg2

changed_table = {1: 'refregerator', 2: 'product'}


def choose_table():
    fill_complete = False
    while (not fill_complete):
        print("CHOOSE TABLE:\n")

        for n, name in changed_table.items(): print("%d:%s" % (n, name))

        answ = input()
        if answ.isdigit():
            answ = int(answ)
            if changed_table.keys().__contains__(answ):
                return answ
            else:
                print("Unexpected value!\n")
                return 0
        else:
            print("Unexpected value!\n")
            return 0


if __name__ == '__main__':
    conn = psycopg2.connect(dbname='refregerator', user='postgres', host='localhost')
    cursor = conn.cursor()

    ti = choose_table()
    while not ti:
        ti = choose_table()

# cursor.execute('SELECT * FROM refregerator')
# records = cursor.fetchall()
# select table_name from information_schema.tables;
# cursor.close()
# conn.close()
