from metastruct import tree_node


def generate_lea_pos(node_db: list,
                     junni_dict: dict = None,
                     round_names: list = None,
                     round_names_prefix: str = None) -> list:
    for i in node_db:
        j = tree_node.TreeNode([i, ])
        print(j.round_num)
    print(round_names)
    return []