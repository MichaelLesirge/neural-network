import enum as _enum

class Action(_enum.Enum):
    SPIN = _enum.auto()
    LEFT = _enum.auto()
    RIGHT = _enum.auto()
    SOFT_DROP = _enum.auto()
    HARD_DROP = _enum.auto()
    HOLD = _enum.auto()

