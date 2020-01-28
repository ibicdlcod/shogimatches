class TableDesc:
    from_cell = (0, 0)
    to_cell = (0, 0)
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
        self.from_cell = from_cell
        self.to_cell = to_cell
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
