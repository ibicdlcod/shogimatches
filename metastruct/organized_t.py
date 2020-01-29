from metastruct import tree_node


class OrganizedTree:
    last_remain_nodes = []
    total_nodes: int = 0
    list_round_prefix = ""
    display_name = list_round_prefix
    list_round_num = []
    node_groups = []

    def __init__(self, matches: list, org_tree_name: str, round_names: list, display_name: str = None):
        self.list_round_prefix = org_tree_name
        self.display_name = self.list_round_prefix if display_name is None else display_name
        self.list_round_num = round_names
        dict1 = dict()
        for i in matches:
            if i.detail3.endswith("局"):
                names = [i.black_name, i.white_name]
                names.sort()
                name_vs = names[0] + ' ' + names[1]
                dict1[i.hash] = name_vs
        dict2 = dict()
        for j in matches:
            if j.hash in dict1.keys():
                if dict1[j.hash] not in dict2.keys():
                    dict2[dict1[j.hash]] = [j, ]
                else:
                    dict2[dict1[j.hash]].append(j)
        tree_nodes = []
        matches2 = matches.copy()
        for k in dict2.keys():
            list_series = dict2[k]
            tree_nodes.append(tree_node.TreeNode(list_series, None, None))
            for m in list_series:
                matches2.remove(m)
        for m in matches2:
            tree_nodes.append(tree_node.TreeNode([m, ], None, None))

        node_group = []
        for i in range(len(self.list_round_num)):
            node_group.append(list())
        for i in range(len(self.list_round_num)):
            for tn in tree_nodes:
                if tn.round_num == (self.list_round_prefix + self.list_round_num[i]):
                    node_group[i].append(tn)
        self.last_remain_nodes = node_group[0]
        self.node_groups = node_group
        for j in range(len(self.list_round_num)):
            for tn in node_group[j]:
                tn_black = tn.black_of_first
                tn_white = tn.white_of_first
                if j == len(self.list_round_num) - 1:
                    continue
                for tn2 in node_group[j + 1]:
                    if tn2.winner().id == tn_black.id:
                        tn.black_q_from = tn2
                    elif tn2.winner().id == tn_white.id:
                        tn.white_q_from = tn2
        self.total_nodes = 0
        for i in range(len(self.list_round_num)):
            self.total_nodes += len(node_group[i])
        self.total_nodes += len(self.last_remain_nodes)


def nodes_layer_from_tr(in_org_tr: OrganizedTree) -> list:  # a list of list of nodes
    return_value = [in_org_tr.last_remain_nodes, ]
    current_nodes = in_org_tr.last_remain_nodes
    while True:
        current_nodes_copy = current_nodes.copy()
        next_layer_content_num = 0
        for tn in current_nodes:
            if tn.black_q_from is not None:
                current_nodes_copy.append(tn.black_q_from)
                next_layer_content_num += 1
            if tn.white_q_from is not None:
                current_nodes_copy.append(tn.white_q_from)
                next_layer_content_num += 1
            current_nodes_copy.remove(tn)
        if next_layer_content_num == 0:
            break
        current_nodes = current_nodes_copy.copy()
        return_value.append(current_nodes)
    return return_value


def split_with_multiple_winners(in_tree: OrganizedTree):
    s = 0
    sub_trees = []
    for last_node in in_tree.last_remain_nodes:
        s += 1
        this_part_nodes = [last_node, ]
        count = [1, ]
        for i in range(1, len(in_tree.list_round_num)):
            count.append(0)
            for node in this_part_nodes:
                if node.black_q_from in in_tree.node_groups[i]:
                    this_part_nodes.append(node.black_q_from)
                    count[i] += 1
                if node.white_q_from in in_tree.node_groups[i]:
                    this_part_nodes.append(node.white_q_from)
                    count[i] += 1
        this_part_matches = []
        for j in this_part_nodes:
            for k in j.series:
                this_part_matches.append(k)
        for j in range(len(in_tree.list_round_num)):
            if count[j] == 0:
                real_depth = j
                break
        else:
            real_depth = len(in_tree.list_round_num)
        sub_org_tree = OrganizedTree(this_part_matches, in_tree.list_round_prefix,
                                     in_tree.list_round_num[:real_depth],
                                     in_tree.list_round_prefix + f"({s})")
        sub_trees.append(sub_org_tree)
    return sub_trees