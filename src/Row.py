# Holds one record
class Row:
    def __init__(self, t: list[str]):
        self.cells = t               # One record
        self.x = None
        self.y = None
        self.dist = None

    def to_string(self) -> str:
        return "{ROW, cells: " + str(self.cells) + " }"