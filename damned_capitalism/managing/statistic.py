from db_generator import choose_variant_from_dict
import os


def store_res_in_party(cursor, account, max_time):
    cursor.execute("(select coalesce(max(party_id)+1,0) from party);")
    party_id = cursor.fetchall()[0][0]
    print("party_id = %d" % party_id)

    cursor.execute("select * from get_ordered_result();")
    for fname, sname, sum_score, spended_money in cursor.fetchall():
        remained_money = account - spended_money

        cursor.execute("insert into party values(%d, %d, %d, '%s','%s',%d,%d,%d)" % (
            party_id, account, max_time, fname, sname, sum_score, spended_money, remained_money))

    cursor.execute("update party set score=0 where remained_money < 0;")


def store_all_parties(cursor, file_name):
    abs_dir = os.path.abspath("../algorithms")
    abs_file = "%s/%s" % (abs_dir, file_name)
    os.system("touch %s" % abs_file)
    os.system("chmod 666 %s" % abs_file)

    cursor.execute("copy (select * from party order by party_id, score) to '%s/%s';" % (abs_dir, file_name))


def store_party_in_file(cursor, file_name, p_id):
    abs_dir = os.path.abspath("../algorithms")
    abs_file = "%s/%s" % (abs_dir, file_name)
    os.system("touch %s" % abs_file)
    os.system("chmod 666 %s" % abs_file)

    cursor.execute("copy (select * from party where party_id = %d order by party_id, score) to '%s/%s';" % (
    p_id, abs_dir, file_name))
