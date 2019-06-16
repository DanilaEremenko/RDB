import json
import time
import subprocess
import os


def run_script(alg_dir, interp, exec, max_time):
    input_path = os.path.abspath("../algorithms/items.json")
    output_path = os.path.abspath("%s/answer.json" % alg_dir)

    cmd_run = "%s %s/%s -i %s -o %s" % \
              (interp, alg_dir, exec, input_path, output_path,)
    print("%s\n" % cmd_run)

    start_time = time.time()

    os.system("rm -f %s" % output_path)
    p = subprocess.Popen(cmd_run, stdout=subprocess.PIPE, shell=True)
    time.sleep(max_time + 0.5)
    p.kill()

    exec_time = time.time() - start_time

    print("%s times = %d\n" % (alg_dir, exec_time))

def parse_cfg_of_alg(path_to_cfg):
    alg_dict = json.load(open(path_to_cfg + "/configuration.json", 'r'))
    return alg_dict.__getitem__("first_name"), alg_dict.__getitem__("second_name"), \
           alg_dict.__getitem__("interp"), alg_dict.__getitem__("exec_name")


def insert_result_to_db(cursor, alg_dir, person_id):
    answer_path = os.path.abspath(alg_dir + "/answer.json")
    no_answer_id = 0
    if os.path.exists(answer_path):
        it_ids = json.load(open(answer_path, 'r')).__getitem__("ids")
        req = "insert into person_item values (default, %d, " % person_id
        for it_id in it_ids:
            cursor.execute(req + "%d);" % it_id)
        os.system("rm %s" % answer_path)
    else:
        print("no %s for player %s" % (answer_path, alg_dir))
        cursor.execute("insert into person_item values (default ,%d,%d)" % (person_id, no_answer_id))


def run_all(cursor, path_to_galg, max_time):
    algs_list = json.load(open(path_to_galg, 'r'))
    person_id = 0
    print("------------------")
    for alg_dir in algs_list:
        alg_dir = "../algorithms/" + alg_dir

        fname, sname, interp, exec = parse_cfg_of_alg(alg_dir)
        cursor.execute("insert into person values(%d, '%s', '%s');" % (person_id, fname, sname))

        run_script(alg_dir, interp, exec, max_time=max_time)

        insert_result_to_db(cursor, alg_dir, person_id)

        person_id += 1

        print("------------------")
