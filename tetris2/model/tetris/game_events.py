import enum as _enum

class Event(_enum.Enum):
    SPIN = _enum.auto()
    LEFT = _enum.auto()
    RIGHT = _enum.auto()
    SOFT_DROP = _enum.auto()
    HARD_DROP = _enum.auto()
    HOLD = _enum.auto()
    
    LINE_CLEAR = _enum.auto()

    # Could add T-SPIN, Perfect Clear, etc
    
