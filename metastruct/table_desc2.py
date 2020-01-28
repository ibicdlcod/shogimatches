class EmptyTable:
    row = 0
    column = 0
    width = 0  # actual width is width + 1

    def __init__(self, row, column, width):
        self.row = row
        self.column = column
        self.width = width

    def __str__(self) -> str:
        return f"White space from ({self.row}, {self.column}) to ({self.row}, {self.column + self.width})"
