import json
import os
import time


def run_script(alg_dir, interp, exec, max_time):
    cmd_run = "%s %s/%s -i ../algorithms/items.json -o %s/answer.json" % \
              (interp, alg_dir, exec, alg_dir,)
    print("run \n%s\n" % cmd_run)

    start_time = time.time()
    os.system(cmd_run)
    exec_time = time.time() - start_time

    if exec_time > max_time + 0.5:
        with open(alg_dir + "/answer.json", "w") as fp:
            json.dump([], fp)


def parse_cfg_of_alg(path_to_cfg):
    alg_dict = json.load(open(path_to_cfg + "/configuration.json", 'r'))
    return alg_dict.__getitem__("first_name"), alg_dict.__getitem__("second_name"), \
           alg_dict.__getitem__("interp"), alg_dict.__getitem__("exec_name")


def insert_result_to_db(cursor, alg_dir, person_id):
    it_ids = json.load(open(alg_dir + "/answer.json", 'r'))
    req = "insert into person_item values (default, %d, " % person_id
    for it_id in it_ids:
        cursor.execute(req + "%d);" % it_id)


def run_all(cursor, path_to_galg, max_time):
    algs_list = json.load(open(path_to_galg, 'r'))
    person_id = 0
    for alg_dir in algs_list:
        alg_dir = "../algorithms/" + alg_dir

        fname, sname, interp, exec = parse_cfg_of_alg(alg_dir)
        cursor.execute("insert into person values(%d, '%s', '%s', 1000);" % (person_id, fname, sname))

        run_script(alg_dir, interp, exec, max_time=max_time)

        insert_result_to_db(cursor, alg_dir, person_id)

        person_id += 1
