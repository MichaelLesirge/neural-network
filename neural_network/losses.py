from abc import ABC, abstractmethod
from typing import Any

import numpy as np

from base import BaseLayer


class Loss(BaseLayer, ABC):
    def __init__(self) -> None:
        super().__init__()
    
