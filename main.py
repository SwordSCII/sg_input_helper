from pynput import mouse, keyboard
from time import sleep
from contextlib import nullcontext
import configparser

config = configparser.ConfigParser()
config.read('key_bindings.config')
PYNPUT_FKEYS = {"f1":keyboard.Key.f1,
                      "f2":keyboard.Key.f2,
                      "f3":keyboard.Key.f3,
                      "f4":keyboard.Key.f4,
                      "f5":keyboard.Key.f5,
                      "f6":keyboard.Key.f6,
                      "f7":keyboard.Key.f7,
                      "f8":keyboard.Key.f8,
                      "f9":keyboard.Key.f9,
                      "f10":keyboard.Key.f10,
                      "f11":keyboard.Key.f11,
                      "f12":keyboard.Key.f12}

keyboard_controller = keyboard.Controller()
SLEEP_TIME = 0.00005
dump_key = config["DEFAULT"]["dump_key"]

#needs to sleep to avoid inputting too quickly and not being detected by system / game
def keyboard_input_with_delay(key, modifier=None):
    with (keyboard_controller.pressed(modifier) if modifier else nullcontext()):
        keyboard_controller.press(key)
        sleep(SLEEP_TIME)
        keyboard_controller.release(key)

def on_click(x, y, button, pressed):
    #simulate centering camera when clicking the icon zone
    #this likely only works for 1920x1080 monitors
    #this also likely only works on setups that use the "main" monitor for the game
    if x > 610 and x < 720 and y < 1060 and y > 890:
        keyboard_input_with_delay(dump_key, modifier=keyboard.Key.ctrl_l)
        keyboard_input_with_delay(dump_key)
        keyboard_input_with_delay(dump_key)

mouse_listener_process = mouse.Listener(on_click=on_click)
mouse_listener_process.start()

camera_hotkeys = {}
for index in range(1,11):
    hotkey_string = config["DEFAULT"]["hotkey_location_"+str(index)]
    #clean data from user
    hotkey_string  = hotkey_string.lower()
    hotkey_input = hotkey_string
    if len(hotkey_string) > 1 and hotkey_string[0] == 'f':
        hotkey_string = f"<{hotkey_string}>"
        hotkey_input = PYNPUT_FKEYS[hotkey_input]
    #currently is hardcoded for shift as modifier for camera location hotkeys
    camera_hotkeys[f'<shift>+{hotkey_string}'] = lambda input=hotkey_input, mod=keyboard.Key.ctrl_l: keyboard_input_with_delay(input,mod)

keyboard_listener_process =  keyboard.GlobalHotKeys(camera_hotkeys)
keyboard_listener_process.start()

print(f"SG Input Helper has started. GLHF") 
try:
    while True:
        sleep(0.5)
except Exception as e:
    keyboard_listener_process.stop()
    mouse_listener_process.stop()
    print(f"Stopping SG Input Helper: {e}")  