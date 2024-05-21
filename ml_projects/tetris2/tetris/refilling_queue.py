from typing import TypeVar, Generic, Iterable
from abc import ABC, abstractmethod
import random

_T = TypeVar("_T")

class RefillingQueue(ABC, Generic[_T]):
    
    def __init__(self, refill_items: Iterable[_T], visible_size: int = 1) -> None:
        self.refill_items = list(refill_items)
        self.visible_size = visible_size

        self.queue = []
        self.fill_queue()
        
    def insert_at_start(self, items: list[_T]) -> None:
        self.queue = items + self.queue
        
    def pop(self) -> _T:
        value = self.queue.pop(0)
        self.fill_queue()
        return value
    
    def view(self) -> list[_T]:
        return self.queue[self.visible_size:]
    
    def fill_queue(self):
        while len(self) < self.visible_size:
            self.queue.append(self.generate())
            
    @abstractmethod
    def generate() -> _T: pass 

class FullRandomQueue(RefillingQueue[_T]):
    def generate(self) -> _T:
        return random.choice(self.refill_items)

class ShuffledBagQueue(RefillingQueue[_T]):
    def __init__(self, refill_items: Iterable[_T], visible_size: int = 1) -> None:
        super().__init__(refill_items, visible_size)
        self.refill_items_shuffled = []
    
    def generate(self) -> _T:
        if len(self.refill_items_shuffled) < 1:
            self.refill_items_shuffled = self.refill_items.copy()
            random.shuffle(self.refill_items_shuffled)
        return self.refill_items_shuffled.pop()

class LessRepeatRandomQueue(RefillingQueue[_T]):
    def __init__(self, refill_items: Iterable[_T], visible_size: int = 1) -> None:
        super().__init__(refill_items, visible_size)
        self.last_item = random.choice(self.refill_items)

    def generate(self) -> _T:
        roll_num = random.randrange(-1, len(self.refill_items))
        if roll_num == -1 or self.refill_items[roll_num] == self.last_item:
            roll_num = random.randrange(0, len(self.refill_items))
        
        self.last_item = self.refill_items[roll_num]
        return self.last_item
