import random
from typing import TypeVar, Generic, Callable, Generator, Iterable

_T = TypeVar("_T")


class RefillingQueue(Generic[_T]):

    def __init__(
        self,
        refill_items: Iterable[_T],
        generator_function: Callable[[_T], Generator[_T, None, None]],
        visible_size: int = 1,
    ) -> None:
        self.refill_items = list(refill_items)
        self.generator_function = generator_function
        self.visible_size = visible_size

        self.queue = []
        self.reset()

    def insert_at_start(self, items: Iterable[_T]) -> None:
        self.queue = list(items) + self.queue

    def pop(self) -> _T:
        value = self.queue.pop(0)
        self.fill_queue()
        return value

    def view(self) -> list[_T]:
        return self.queue[self.visible_size :]

    def reset(self) -> None:
        self.queue.clear()
        self.generator = self.generator_function(self.refill_items)
        self.fill_queue()

    def fill_queue(self):
        while len(self.queue) < self.visible_size:
            self.queue.append(next(self.generator))


def full_random_generator(items: list[_T]) -> Generator[_T, None, None]:
    while True:
        yield random.choice(items)


def shuffled_double_bag_generator(items: list[_T]) -> Generator[_T, None, None]:
    items = items.copy()
    while True:
        yield from items
        random.shuffle(items)


def shuffled_double_bag_generator(items: list[_T]) -> Generator[_T, None, None]:
    items = items + items
    while True:
        yield from items
        random.shuffle(items)


def less_repeat_random_generator(items: list[_T]) -> Generator[_T, None, None]:
    last_num = None
    while True:
        roll_num = random.randrange(-1, len(items))

        if roll_num in (-1, last_num):
            roll_num = random.randrange(0, len(items))

        last_num = roll_num
        yield items[roll_num]
