import argparse
import sys
import time
import json


def filling_algorithm(max_time, ids, prices, values, account):
    s_time = time.time()
    # ---------------- calculate answer ---------------------------
    while (time.time() - s_time) < max_time:
        answer = [1, 2, 3, 4]

    return answer


if __name__ == '__main__':
    # ------------------ parsing arguments for connection creating -----------------------
    need_args = 5

    if sys.argv.__len__() != need_args:
        raise Exception("Illegal amount of arguments != %d" % need_args)
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input_file", type=str,
                        help="password for user")

    parser.add_argument("-o", "--output_file", type=str,
                        help="your bank account")

    args = parser.parse_args()

    game_dict = json.load(open(args.input_file, 'r'))

    selected_ids = filling_algorithm(
        max_time=game_dict.__getitem__("max_time"),
        account=game_dict.__getitem__("account"),
        ids=game_dict.__getitem__("ids"),
        prices=game_dict.__getitem__("prices"),
        values=game_dict.__getitem__("values")
    )

    with open(args.output_file, "w") as fp:
        json.dump(selected_ids, fp)
