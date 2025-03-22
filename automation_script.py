import pyautogui
import cv2
import numpy as np
import time
import json
import os
import sys
import subprocess
import pygetwindow

CONFIG_FILE = "gui_config.json"

def find_and_interact(image_path, action, text=None, wait_time=0, confidence=0.8):
    """Finds an image on the screen and performs the specified action"""
    """Finds an image on the screen and performs the specified action"""
    absolute_image_path = os.path.join(os.getcwd(), image_path)
    #absolute_image_path = image_path

    # Handle special key actions without image processing
    special_keys = ["left", "right", "up", "down", "esc", "enter"]
    if any(key in action for key in special_keys):
        for key_action in action:
            if key_action == "left":
                print("pressing left arrow")
                pyautogui.press("left")
            elif key_action == "right":
                print(" pressing right arrow")
                pyautogui.press("right")
            elif key_action == "up":
                print(" pressing up arrow")
                pyautogui.press("up")
            elif key_action == "down":
                print(" pressing down arrow")
                pyautogui.press("down")
            elif key_action == "esc":
                print(" pressing escape")
                pyautogui.press("escape")
            elif key_action == "enter":
                print(" pressing enter")
                pyautogui.press("enter")
        return True

    # Bypass image check for "Type Text" action
    if isinstance(action, dict) and action.get("type") and not image_path:
        print(f" typing text: {text} without image check")
        pyautogui.typewrite(text)
        return True

    print(f"🔍 Checking for image: {image_path}")

    # Standard image-based actions
    if not os.path.exists(image_path):
        print(f"⚠️ Image not found: {image_path}")
        return False
    
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    try:
        template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if template is None:
            print(f"❌ OpenCV failed to load image: {image_path}. Check if the file exists and is a valid image format.")
            return False
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    except Exception as e:
        print(f"❌ Error loading or processing image ({image_path}): {e}. Details: {str(e)}")
        return False

    if max_val >= confidence:
        x, y = max_loc
        w, h = template.shape[1], template.shape[0]
        center_x, center_y = x + w // 2, y + h // 2

        print(f"✅ Found ({image_path}) at ({center_x}, {center_y}), executing: {action}...")

        pyautogui.moveTo(center_x, center_y, duration=0.2)

        if isinstance(action, dict):
            if action.get("click"):
                print("🖱️ Clicking")
                pyautogui.click()

            if action.get("hover"):
                print(" hovering")
                pyautogui.moveTo(center_x, center_y)

            if action.get("type") and text:
                print(f" typing text: {text}")
                pyautogui.typewrite(text)
        elif isinstance(action, list):
            if "click" in action:
                print("🖱️ Clicking")
                pyautogui.click()
            if "hover" in action:
                print(" hovering")
                pyautogui.moveTo(center_x, center_y)
            if "left" in action:
                print(" pressing left arrow")
                pyautogui.press("left arrow")
            if "right" in action:
                print(" pressing right arrow")
                pyautogui.press("right arrow")
            if "up" in action:
                print(" pressing up arrow")
                pyautogui.press("up arrow")
            if "down" in action:
                print(" pressing down arrow")
                pyautogui.press("down arrow")

        if wait_time:
            print(f" waiting for {wait_time} seconds")
            time.sleep(float(wait_time))

        return True
    else:
        print(f"❌ Image ({image_path}) not found")
        return False

def load_actions_from_file():
    """Load actions from the config file"""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Config file not found: {CONFIG_FILE}")
        return []
    except json.JSONDecodeError:
        print("❌ Invalid JSON data in config file.")
        return []

def main():
    """Runs the automation sequence"""
    # Change the working directory to the script's directory
    try:
        os.chdir(sys._MEIPASS)
    except AttributeError:
        pass
    time.sleep(10)  # Wait 10 seconds before image search

    # Load button_actions from command-line argument or config file
    if len(sys.argv) > 1:
        try:
            # Check if the argument is a file path
            if os.path.exists(sys.argv[1]):
                with open(sys.argv[1], "r", encoding="utf-8") as f:
                    button_actions = json.load(f)
            else:
                button_actions = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            print("❌ Invalid JSON data provided.")
            return
        except FileNotFoundError:
            print(f"❌ File not found: {sys.argv[1]}")
            return
    else:
        button_actions = load_actions_from_file()
        if not button_actions:
            print("⚠️ No actions provided.")
            return

    for button in button_actions:
        action = button["actions"][0] if button["actions"] else None
        text = button.get("text")
        wait_time = button.get("wait_time")
        image = button.get("image")
        executable_path = button.get("executable_path")

        if action == "execute" and executable_path:
            print(f" executing: {executable_path}")
            subprocess.Popen(f'"{executable_path}"', shell=True)
            time.sleep(float(wait_time) if wait_time else 1)  # Wait for the application to open
            notepad_window = pyautogui.getWindowsWithTitle("Notepad")
            if isinstance(notepad_window, list) and notepad_window:
                # Check if the window is already active
                if notepad_window and len(notepad_window) > 0:
                    if isinstance(notepad_window[0], pyautogui.Window):
                        try:
                            if not notepad_window[0].isActive():
                                time.sleep(1)  # Add a short delay
                                try:
                                    notepad_window[0].activate()
                                except pygetwindow.PyGetWindowException as e:
                                    print(f"PyGetWindowException caught: {e}")
                        except TypeError:
                            print("TypeError caught: Assuming window is not active")
                            time.sleep(1)  # Add a short delay
                            try:
                                notepad_window[0].activate()
                            except pygetwindow.PyGetWindowException as e:
                                print(f"PyGetWindowException caught: {e}")
        elif action == "wait":
            print(f" waiting for {wait_time} seconds")
            time.sleep(float(wait_time))
        elif action == "type_text":
            if image:
                find_and_interact(image, {"type": True}, text=text, wait_time=wait_time)
            else:
                print(f" typing text: {text} without image check")
                pyautogui.typewrite(text)
        else:
            find_and_interact(image, button["actions"], text=text, wait_time=wait_time)
        time.sleep(1)

if __name__ == "__main__":
    main()
