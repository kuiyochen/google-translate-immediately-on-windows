import time
import threading

import pyperclip
import ctypes
from googletrans import Translator

translator = Translator()
# print(translated.text)
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

##### https://stackoverflow.com/questions/14685999/trigger-an-event-when-clipboard-content-changes
class ClipboardWatcher(threading.Thread):
    def __init__(self):
        super(ClipboardWatcher, self).__init__()
        self._stopping = False

    def run(self):
        recent_value = ""
        while True:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                print("Value changed: %s" % str(recent_value))
                translated = translator.translate(str(recent_value), src='en', dest='zh-tw') # tc
                Mbox('translator', translated.text, 1)
            time.sleep(0.1)

    def stop(self):
        self._stopping = True

def main():
    watcher = ClipboardWatcher()
    watcher.start()
    while True:
        try:
            print("Waiting for changed clipboard...")
            time.sleep(10)
        except KeyboardInterrupt:
            watcher.stop()
            break


if __name__ == "__main__":
    main()