from db_generator import choose_variant_from_dict
import os


def show_results(cursor):
    abs_respath = os.path.abspath("../algorithms")

    cursor.execute("copy (select * from get_ordered_result()) to '%s/%s';" % (abs_respath, "result.txt"))

    cursor.execute("copy (select * from get_item_person()) to '%s/%s';" % (abs_respath, "result_full.txt"))
