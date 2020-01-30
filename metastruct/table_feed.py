from bracketgen import bra_from_tr
from metastruct import organized_t


class TableFeed:
    tree: organized_t.OrganizedTree = None,
    prefix: str = ''
    tournament_name: str = ''
    iteration: str = ''
    out_seed_disabled: bool = False
    in_seed_disabled: bool = False
    first_place_label: str = ''
    second_place_label: str = ''

    def __init__(self, in_tree,
                 prefix,
                 tournament_name: str,
                 iteration: str,
                 out_seed_disable,
                 in_seed_disable,
                 first_place_labels,
                 second_place_labels):
        self.tree = in_tree
        self.prefix = prefix
        self.tournament_name = tournament_name
        self.iteration = iteration
        self.out_seed_disabled = out_seed_disable
        self.in_seed_disabled = in_seed_disable
        self.first_place_label = first_place_labels
        self.second_place_label = second_place_labels


def draw_table_from_feed(feeds: list) -> str:
    result = ""
    for feed in feeds:
        result += feed.prefix
        in_tree = feed.tree
        table = bra_from_tr.generate_bra_pos(in_tree,
                                             dict(),
                                             dict(),
                                             feed.out_seed_disabled,
                                             feed.in_seed_disabled,
                                             feed.first_place_label,
                                             feed.second_place_label)
        draw_table = bra_from_tr.draw_table(table,
                                            feed.tournament_name
                                            + feed.iteration
                                            + in_tree.display_name
                                            )
        result += draw_table
    return result
