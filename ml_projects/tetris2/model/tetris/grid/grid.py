from typing import Generator, Self

import numpy as np

CoordinatePair = tuple[int, int]
WidthHeightPair = tuple[int, int]

def find_corners(grid: np.ndarray, null_value=0) -> tuple[CoordinatePair, CoordinatePair]:
    empty_positions = np.where(grid != null_value)
    y_start = min(empty_positions[0])
    y_end = max(empty_positions[0]) + 1
    x_start = min(empty_positions[1])
    x_end = max(empty_positions[1]) + 1
    return ((x_start, y_start), (x_end, y_end))


class Grid:
    def __init__(self, grid: np.ndarray, null_value=0) -> None:
        self.grid = grid
        self.null_value = null_value
        self.clear()

    @classmethod
    def empty(cls, shape: WidthHeightPair, null_value=0, dtype=int) -> Self:
        width, height = shape
        new = cls(np.empty((height, width), dtype=dtype), null_value)
        new.clear()
        return new

    @classmethod
    def empty_like(cls, prototype: Self) -> Self:
        new = cls(np.empty_like(prototype.get_grid_array()), prototype.get_null_value())
        new.clear()
        return new

    def clear(self) -> None:
        self.grid.fill(self.null_value)

    def get_grid_array(self) -> np.ndarray:
        return self.grid

    def get_null_value(self) -> np.ndarray:
        return self.null_value

    def insert(self, position: CoordinatePair, subgrid: np.ndarray) -> None:
        """Put subgrid at specified position in main grid, EMPTY values will not be set"""

        x, y = position

        ((x_start, y_start), (x_end, y_end)) = find_corners(subgrid)

        subgrid = subgrid[y_start:y_end, x_start:x_end]
        x, y = x + x_start, y + y_start
        width, height = x_end - x_start, y_end - y_start

        view = self.grid[y : y + height, x : x + width]
        mask = subgrid != self.null_value
        view[mask] = subgrid[mask]

    def insert_if_empty(self, position: CoordinatePair, subgrid: np.ndarray) -> bool:
        """if subgrid does not overlap, insert it and return true"""
        x, y = position

        ((x_start, y_start), (x_end, y_end)) = find_corners(subgrid)

        subgrid = subgrid[y_start:y_end, x_start:x_end]
        x, y = x + x_start, y + y_start
        width, height = x_end - x_start, y_end - y_start

        view = self.grid[y : y + height, x : x + width]

        if view.shape != subgrid.shape:
            return False

        mask = subgrid != self.null_value

        # Check to see if there is any overlap
        if np.logical_and(view[mask], subgrid[mask]).any():
            return False

        # Set values in grid by setting view
        view[mask] = subgrid[mask]
        return True

    def insert_empty(
        self, position: CoordinatePair, subgrid_mask: np.ndarray[bool]
    ) -> None:
        """Clear all values at specified position where subgrid_mask is True"""
        x, y = position
        height, width = subgrid_mask.shape

        view = self.grid[y : y + height, x : x + width]
        view[subgrid_mask.astype(bool)] = 0

    def does_overlap(self, position: CoordinatePair, subgrid: np.ndarray) -> bool:
        """check if subgrid overlaps with anything in grid at specified position"""
        x, y = position

        ((x_start, y_start), (x_end, y_end)) = find_corners(subgrid)

        subgrid = subgrid[y_start:y_end, x_start:x_end]
        x, y = x + x_start, y + y_start
        width, height = x_end - x_start, y_end - y_start

        view = self.grid[y : y + height, x : x + width]

        if view.shape != subgrid.shape:
            return True

        mask = subgrid != self.null_value

        # Check to see if there is any overlap
        return np.logical_and(view[mask], subgrid[mask]).any()

    def get_grid_string(
        self, row_template_str="[%s]", full_tile_template_str=" %s", empty_tile_str="  "
    ) -> str:

        return "\n".join(
            row_template_str
            % (
                "".join(
                    (
                        full_tile_template_str % item
                        if (item != self.null_value)
                        else empty_tile_str
                    )
                    for item in row
                )
            )
            for row in self.grid
        )

    def get_height(self) -> int:
        return self.grid.shape[0]

    def get_width(self) -> int:
        return self.grid.shape[1]

    def copy(self):
        return self.__class__(self.grid.copy(), self.null_value)

    def __iter__(self) -> Generator[tuple[int, CoordinatePair], None, None]:
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                yield (self.grid[row, col], (row, col))

    def __str__(self) -> str:
        return self.get_grid_string()
