from db_generator import choose_variant_from_dict

avail_stat_dict = {0: 'common statistic', 1: 'most economical', 2: 'most wasteful', 99: 'exit'}


def get_stat():
    go_back = False

    while not go_back:
        stat_i = choose_variant_from_dict("AVAILABLE STATISTIC:", avail_stat_dict)

        if stat_i == 0:
            print('TODO run script for common statistic\n')
        elif stat_i == 1:
            print("TODO run script for most economical\n")
        elif stat_i == 2:
            print("TODO run script for most wasteful\n")

        elif stat_i == 99:
            go_back = True
