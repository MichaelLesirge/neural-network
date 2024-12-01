import pyautogui
import webbrowser
import numpy as np

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

def setup():
    webbrowser.Mozilla("C:\\Program Files\\Mozilla Firefox\\firefox.exe").open("https://tetris.com/play-tetris/")
    pyautogui.sleep(3)
    pyautogui.moveTo(1910, 208)
    pyautogui.mouseDown(button='left')
    pyautogui.moveRel(0, 90, duration=0.1)
    pyautogui.mouseUp(button='left')
    pyautogui.leftClick(966, 442)
    pyautogui.sleep(3)
    pyautogui.leftClick(966, 442)
    pyautogui.sleep(4)

def left():
    pyautogui.keyDown('left')

def right():
    pyautogui.keyDown('right')

def soft_drop():
    pyautogui.keyDown('down')

def hard_drop():
    pyautogui.keyDown('space')

def rotate():
    pyautogui.keyDown('up')

def hold():
    pyautogui.keyDown('c')

LEFT = 815
TOP = 218
CELL_SIZE = 32

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

def get_luminance(color):
    return 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]

def get_board():
    board = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            color = pyautogui.pixel(LEFT + col * CELL_SIZE, TOP + row * CELL_SIZE)
            board[row, col] = get_luminance(color) > 15
            
    return board

setup()
print(get_board())