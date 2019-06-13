from db_generator import choose_variant_from_dict

avail_stat_dict = {0: 'most economical', 1: 'most wasteful'}


def get_stat():
    choose_variant_from_dict("AVAILABLE ACTIONS:", avail_stat_dict)



