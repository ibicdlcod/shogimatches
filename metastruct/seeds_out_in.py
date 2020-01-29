from metastruct import organized_t


class Seed:
    seed_type: int = 0
    left_tree_list: list = None,
    right_tree_list: list = None,
    character_set: list = [],
    character_set_out: list = None,
    seed_dict: dict = None

    def __init__(self,
                 seed_type,
                 left_tree_list: list,
                 right_tree_list: list,
                 character_set: list,
                 character_set_out: list = None,
                 seed_dict: dict = None):
        self.seed_type = seed_type
        self.left_tree_list = left_tree_list
        self.right_tree_list = right_tree_list
        self.character_set = character_set
        self.character_set_out = self.character_set if character_set_out is None else character_set_out
        self.seed_dict = None if not (seed_type == 0 or seed_type == 5) else seed_dict

    def assign_seed(self):
        if self.seed_type == 0:
            pass
        elif self.seed_type == 5:
            pass
        else:
            self.assign_seed_intersect()

    def assign_seed_intersect(self):
        left_kishi = []
        right_kishi = []
        for right_tree in self.right_tree_list:
            right_kishi += (right_tree.get_winners()
                            + right_tree.get_runners_up()
                            + right_tree.get_others())
        if self.seed_type == 1:
            for left_tree in self.left_tree_list:
                for winner in left_tree.get_winners():
                    left_kishi.append(winner)
        elif self.seed_type == 2:
            for left_tree in self.left_tree_list:
                for loser in left_tree.get_runners_up():
                    left_kishi.append(loser)
        elif self.seed_type == -1:
            for left_tree in self.left_tree_list:
                for loser in left_tree.get_runners_up():
                    left_kishi.append(loser)
                for loser in left_tree.get_others():
                    left_kishi.append(loser)
        elif self.seed_type == -2:
            for left_tree in self.left_tree_list:
                for loser in left_tree.get_others():
                    left_kishi.append(loser)

        intersect_kishi = list(set(left_kishi).intersection(set(right_kishi)))
        dict_left = dict()
        dict_right = dict()
        for i in range(len(intersect_kishi)):
            print(intersect_kishi[i].fullname)
            dict_left[intersect_kishi[i].id] = self.character_set[i]
            dict_right[intersect_kishi[i].id] = self.character_set_out[i]
        print(dict_left)
        print(dict_right)
        left_tree.out_seed = dict_left
        right_tree.in_seed = dict_right
