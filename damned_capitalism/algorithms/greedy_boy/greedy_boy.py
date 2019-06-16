import argparse
import sys
import time
import json
from Item import Item


def filling_algorithm(max_time, ids, prices, values, account, time_start):
    items = []
    for id, price, value in zip(ids, prices, values):
        items.append(Item(id, price, value))
    items.sort()
    items.reverse()

    selected_price = 0
    selected_ids = []
    i = 0
    for cur_item in items:
        if (time.time() - time_start) < max_time:
            if (selected_price + cur_item.price) < account:
                selected_ids.append(cur_item.id)
                selected_price += cur_item.price

        else:
            return (selected_ids, i)
        i += 1
    return (selected_ids, i)


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

    selected_ids, last_id = filling_algorithm(
        max_time=game_dict.__getitem__("max_time"),
        account=game_dict.__getitem__("account"),
        ids=game_dict.__getitem__("ids"),
        prices=game_dict.__getitem__("prices"),
        values=game_dict.__getitem__("values"),
        time_start=time.time()
    )

    answer = {"ids": selected_ids, "ids.size": selected_ids.__len__(), "last_id": last_id}
    with open(args.output_file, "w") as fp:
        json.dump(answer, fp)
