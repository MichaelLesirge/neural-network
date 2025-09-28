from abc import ABC, abstractmethod
import random
from typing import TypeVar, Generic, Iterable

_T = TypeVar("_T")


class RefillingQueue(ABC, Generic[_T]):

    def __init__(self, refill_items: Iterable[_T], visible_size: int = 1) -> None:
        self.refill_items = list(refill_items)
        self.visible_size = visible_size

        self.queue = []
        self.reset()

    def get_view_size(self) -> int:
        return self.visible_size

    def insert_at_start(self, items: list[_T]) -> None:
        self.queue = items + self.queue

    def pop(self) -> _T:
        value = self.queue.pop(0)
        self.fill_queue()
        return value

    def view(self) -> list[_T]:
        return self.queue[-self.visible_size :]

    def reset(self) -> None:
        self.queue.clear()
        self.fill_queue()

    def fill_queue(self):
        while len(self.queue) < self.visible_size:
            self.queue.append(self.generate())

    @abstractmethod
    def generate() -> _T:
        pass


class FullRandomQueue(RefillingQueue[_T]):
    def generate(self) -> _T:
        return random.choice(self.refill_items)


class ShuffledBagQueue(RefillingQueue[_T]):

    def reset(self) -> None:
        self.refill_items_shuffled = []
        super().reset()

    def generate(self) -> _T:
        if len(self.refill_items_shuffled) < 1:
            self.refill_items_shuffled = self.refill_items.copy()
            random.shuffle(self.refill_items_shuffled)
        return self.refill_items_shuffled.pop()


class ShuffledDoubledBagQueue(RefillingQueue[_T]):

    def reset(self) -> None:
        self.refill_items_shuffled = []
        super().reset()

    def generate(self) -> _T:
        if len(self.refill_items_shuffled) < 1:
            self.refill_items_shuffled = self.refill_items + self.refill_items
            random.shuffle(self.refill_items_shuffled)
        return self.refill_items_shuffled.pop()


class LessRepeatRandomQueue(RefillingQueue[_T]):

    def reset(self) -> None:
        self.last_roll_num = None
        super().reset()

    def generate(self) -> _T:
        roll_num = random.randrange(-1, len(self.refill_items))
        if roll_num in (-1, self.last_roll_num):
            roll_num = random.randrange(0, len(self.refill_items))

        self.last_roll_num = roll_num
        return self.refill_items[roll_num]
