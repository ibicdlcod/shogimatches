class TableDesc:
    from_cell = [0, 0]
    to_cell = [0, 0]
    empty = False
    content = ''
    content_len = 0
    bg_color = '#FFFFFF'
    border_black = False  # default or black
    border_up = False
    border_right = False
    border_down = False
    border_left = False
    '''
    default: style="border:1px solid #aaa”
    上右下左 style="border-width:2px 2px 2px 0; border-style:solid; border-color:black;"
    '''

    def __init__(self,
                 from_cell: tuple = (0, 0),
                 to_cell: tuple = (0, 0),
                 empty=False,
                 content: str = '',
                 bg_color: str = '#FFFFFF',
                 border_black: bool = False,
                 border_active: tuple = (False, False, False, False),
                 content_len=-1
                 ):
        self.from_cell = list(from_cell)
        self.to_cell = list(to_cell)
        self.empty = empty
        self.content = content
        self.content_len = content_len if content_len != -1 else len(content)
        self.bg_color = bg_color
        self.border_black = border_black
        self.border_up = border_active[0]
        self.border_right = border_active[1]
        self.border_down = border_active[2]
        self.border_left = border_active[3]

    def __str__(self):
        out_str_item = [
            str(self.from_cell),
            str(self.to_cell),
            str(self.empty),
            self.content,
            str(self.content_len),
            self.bg_color,
            str(self.border_black),
            str(self.border_up),
            str(self.border_right),
            str(self.border_down),
            str(self.border_left)
        ]
        return ",".join(out_str_item)

    def shift(self, row_shift: int, col_shift: int):
        self.from_cell[0] += row_shift
        self.to_cell[0] += row_shift
        self.from_cell[1] += col_shift
        self.to_cell[1] += col_shift


def union_table(in_table_list_list: list) -> list:
    column_limit = 0
    for in_table_list in in_table_list_list:
        column_limit_item = max([in_table.to_cell[1] for in_table in in_table_list]) + 1
        if column_limit < column_limit_item:
            column_limit = column_limit_item
    print(column_limit)
    row_limit = 0
    for in_table_list in in_table_list_list:
        row_limit_item = max([in_table.to_cell[0] for in_table in in_table_list]) + 1
        row_limit += row_limit_item
    print(row_limit)
    for in_table_list in in_table_list_list:
        this_column_limit = max([in_table.to_cell[1] for in_table in in_table_list]) + 1
        for cell in in_table_list:
            cell.shift(0, column_limit - this_column_limit)
    # for i in in_table_list_list[0]:
    #     print(i)
    # print()
    row_current = 0
    for in_table_list in in_table_list_list:
        for cell in in_table_list:
            cell.shift(row_current, 0)
        row_current += max([in_table.to_cell[0] for in_table in in_table_list]) + 1
    return_result = []
    for in_table_list in in_table_list_list:
        for cell in in_table_list:
            return_result.append(cell)
    return_result.sort(key=lambda cell: (cell.from_cell[0], cell.from_cell[1]))
    for i in return_result:
        print(i)
    return return_result


def padding_0(table_pos_all: list) -> list:
    occupied_grid = []
    row_limit = max([cell.to_cell[0] for cell in table_pos_all]) + 1
    column_limit = max([cell.to_cell[1] for cell in table_pos_all]) + 1
    for i in range(row_limit):
        occupied_grid.append([])
        for j in range(column_limit):
            occupied_grid[i].append(False)
    for cell in table_pos_all:
        from_row = cell.from_cell[0]
        from_col = cell.from_cell[1]
        to_row = cell.to_cell[0] + 1
        to_col = cell.to_cell[1] + 1
        for i in range(from_row, to_row):
            for j in range(from_col, to_col):
                occupied_grid[i][j] = True
    for i in range(row_limit):
        j = 0
        while j < column_limit:
            if not occupied_grid[i][j]:
                k = j
                while k < column_limit - 1:
                    if occupied_grid[i][k + 1]:
                        break
                    k += 1
                t7 = TableDesc(
                    (i, j),
                    (i, k),
                    True,
                )
                table_pos_all.append(t7)
                j = k + 1
            else:
                j += 1
    table_pos_all.sort(key=lambda cell: (cell.from_cell[0], cell.from_cell[1]))
    return table_pos_all
