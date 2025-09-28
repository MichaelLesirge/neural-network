import pyautogui
import keyboard

def get_coords():
    print(pyautogui.position())

# print coords of mouse cursor when ctrl+q is pressed
was_pressed = False
while True:
    if keyboard.is_pressed('ctrl+q'):
        if not was_pressed:
            get_coords()
            was_pressed = True
    else:
        was_pressed = False
