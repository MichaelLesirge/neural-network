import pathlib

import numpy as np
import pygame

MAX_ROTATIONS = 4

ALL_SHAPES: list["TetrominoBlockShape"] = []
SHAPE_ID_MAP: dict[int, "TetrominoBlockShape"] = {}

def rotate(shape):
    return np.flip(np.rot90(shape))

class TetrominoBlockShape:

    def __init__(self, name: str, color: pygame.Color, shape: list[list[int]] | np.ndarray, rotator = rotate) -> None:

        self.name = name
        self.color = color
        self.id = len(ALL_SHAPES) + 1

        parent_path = pathlib.Path(__file__).parent
        
        self.image = pygame.image.load(parent_path / "normal-tetromino" / f"{self.name}.png")
        self.image_ghost = pygame.image.load(parent_path / "ghost-tetromino" / f"{self.name}.png")

        ALL_SHAPES.append(self)
        SHAPE_ID_MAP[self.id] = self

        shape = np.array(shape, dtype=np.uint8)

        self.rotations: list[np.ndarray] = []
        for i in range(MAX_ROTATIONS):
            self.rotations.append(shape)
            shape = rotator(shape)
            if np.array_equal(shape, self.rotations[0]):
                break

    def get_name(self) -> str: return self.name

    def get_color(self) -> pygame.Color: return self.color

    def get_id(self) -> int: return self.id

    def get_num_of_rotations(self) -> int: return len(self.rotations)
    
    def get_largest_dimension(self) -> int: return max(self.rotations[0].shape)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.color}, {self.rotations[0]})"


TetrominoBlockShape("I", (0, 240, 240), [
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]),

TetrominoBlockShape("O", (240, 240, 0), [
    [1, 1],
    [1, 1],
]),

TetrominoBlockShape("L", (240, 160, 0), [
    [1, 1, 0],
    [0, 1, 0],
    [0, 1, 0],
]),

TetrominoBlockShape("J", (0, 0, 240), [
    [0, 1, 1],
    [0, 1, 0],
    [0, 1, 0],
]),

TetrominoBlockShape("T", (160, 0, 240), [
    [0, 1, 0],
    [1, 1, 1],
    [0, 0, 0],
]),

TetrominoBlockShape("Z", (240, 0, 0), [
    [0, 0, 0],
    [1, 1, 0],
    [0, 1, 1],
]),

TetrominoBlockShape("S", (0, 240, 0), [
    [0, 0, 0],
    [0, 1, 1],
    [1, 1, 0],
]),


def main() -> None:
    states = [" .", "██"]

    for shape in ALL_SHAPES:
        print(shape.name + ": ")
        for i, orientations in enumerate(shape.rotations):
            print()
            print("\n".join(
                "".join(states[value] for value in row) for row in orientations
            ))
        print()


if __name__ == "__main__":
    main()
