from db_generator import choose_variant_from_dict


def show_results(cursor):
    cursor.execute("select * from order_by_score();")
    result = cursor.fetchall()
    print("fname\t\t\tsname\t\t\t\t\tscore")
    for fname, sname, score in result:
        print("%s\t\t\t%s\t\t\t%d" % (fname, sname, score))
