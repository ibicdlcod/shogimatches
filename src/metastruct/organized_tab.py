from metastruct import table_desc


class OrganizedTable:
    table_list = []
    column_disabled_dict = dict()

    def __init__(self, table_list, column_disabled_dict):
        self.table_list = table_list
        self.column_disabled_dict = column_disabled_dict

    def process_disabled_dict(self):
        return_list = []
        for cell in self.table_list:
            from_col = cell.from_cell[1]
            to_col = cell.to_cell[1]
            disabled_col_from_num = 0
            for i in range(from_col):
                if i in self.column_disabled_dict and self.column_disabled_dict[i]:
                    disabled_col_from_num += 1
            from_col -= disabled_col_from_num
            disable_col_to_num = 0
            for i in range(to_col + 1):
                if i in self.column_disabled_dict and self.column_disabled_dict[i]:
                    disable_col_to_num += 1
            to_col -= disable_col_to_num
            cell.from_cell[1] = from_col
            cell.to_cell[1] = to_col
            if from_col <= to_col:
                return_list.append(cell)
        self.table_list = return_list


def union_table_with_dict(in_org_table_list_list: list) -> OrganizedTable:
    column_limit = 0
    for in_org_table in in_org_table_list_list:
        in_table_list = in_org_table.table_list
        column_limit_item = max([in_table.to_cell[1] for in_table in in_table_list]) + 1
        if column_limit < column_limit_item:
            column_limit = column_limit_item
    row_limit = 0
    for in_org_table in in_org_table_list_list:
        in_table_list = in_org_table.table_list
        row_limit_item = max([in_table.to_cell[0] for in_table in in_table_list]) + 1
        row_limit += row_limit_item

    for in_org_table in in_org_table_list_list:
        in_table_list = in_org_table.table_list
        column_disabled_dic = in_org_table.column_disabled_dict
        this_column_limit = max([in_table.to_cell[1] for in_table in in_table_list]) + 1
        for cell in in_table_list:
            cell.shift(0, column_limit - this_column_limit)
        new_column_disabled_dic = dict()
        for k, v in column_disabled_dic.items():
            new_column_disabled_dic[k + column_limit - this_column_limit] = v
        in_org_table.column_disabled_dict = new_column_disabled_dic
    row_current = 0
    for in_org_table in in_org_table_list_list:
        in_table_list = in_org_table.table_list
        for cell in in_table_list:
            cell.shift(row_current, 0)
        row_current += max([in_table.to_cell[0] for in_table in in_table_list]) + 2
    return_result = []

    new_column_disabled_dic = dict()
    for in_org_table in in_org_table_list_list:
        in_table_list = in_org_table.table_list
        column_disabled_dic = in_org_table.column_disabled_dict
        for cell in in_table_list:
            return_result.append(cell)
        for k, v in column_disabled_dic.items():
            if k not in new_column_disabled_dic:
                new_column_disabled_dic[k] = v
            else:
                if new_column_disabled_dic[k] and (not column_disabled_dic[k]):
                    new_column_disabled_dic[k] = False

    return_result = table_desc.padding_0(return_result)
    return_result.sort(key=lambda cell_1: (cell_1.from_cell[0], cell_1.from_cell[1]))
    return OrganizedTable(return_result, new_column_disabled_dic)
