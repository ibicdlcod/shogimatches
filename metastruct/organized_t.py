from metastruct import tree_node


class OrganizedTree:
    last_remain_nodes = []
    list_round_prefix = ""
    list_round_num = []

    def __init__(self, matches: list, org_tree_name: str, round_names: list):
        self.list_round_prefix = org_tree_name
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
        for j in range(len(self.list_round_num)):
            for tn in node_group[j]:
                tn_black = tn.black_of_first
                tn_white = tn.white_of_first
                if j == len(self.list_round_num) - 1:
                    continue
                for tn2 in node_group[j + 1]:
                    if tn2.winner().id == tn_black.id:
                        tn.black_q_from = tn2
                        break
                    elif tn2.winner().id == tn_white.id:
                        tn.white_q_from = tn2
                        break
        for i in range(len(self.list_round_num)):
            for tn in node_group[i]:
                print(tn)
            print()
