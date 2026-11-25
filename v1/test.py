from pynput import keyboard
import time

DOUBLE_CMD_WINDOW = 0.4
DOUBLE_PRESS_TIMEOUT = 0.6

state = "IDLE"
last_cmd_time = 0
_time = 0
locked = False


def trigger_first():
    global locked
    locked = True

    locked = False

def reset():
    global state
    state = "IDLE"


def on_press(key):
    global state, last_cmd_time, _time, locked
    if locked:
        return

    now = time.time()

    if key in (keyboard.Key.cmd, keyboard.Key.cmd_r):
        if now - last_cmd_time <= DOUBLE_CMD_WINDOW:
            state = "DETECTED"
            _time = now
        last_cmd_time = now


def watchdog():
    global state, _time

    while True:
        if state == "DETECTED" and time.time() - _time > DOUBLE_PRESS_TIMEOUT:
            trigger_first()
            reset()

        time.sleep(0.05)


import threading
threading.Thread(target=watchdog, daemon=True).start()

with keyboard.Listener(on_press=on_press) as listener:
    print("Listening for Cmd x2 then '/' ...")
    listener.join()