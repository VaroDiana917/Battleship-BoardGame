from dataclasses import dataclass


@dataclass
class Cell:
    row: int
    column: int
    ship: bool
    checked: bool
