import time
import os
import threading

import pyperclip
import ctypes
from googletrans import Translator
from PIL import ImageGrab
from PIL import Image
import pytesseract
# import cv2
import numpy as np

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
            try:
                if type(tmp_value) == type(ImageGrab.grabclipboard()):
                    raise TypeError()
                tmp_value = pyperclip.paste()
                if tmp_value != recent_value:
                    recent_value = tmp_value
                    recent_value = str(recent_value)
                    print("Value changed: %s" % recent_value)
                    translated = translator.translate(recent_value, src='en', dest='zh-tw') # tc
                    Mbox('translator', "\n".join([recent_value, translated.text]), 1)
            except:
                try:
                    tmp_value = ImageGrab.grabclipboard()
                    if type(tmp_value) != type(recent_value) or tmp_value.size[0] != recent_value.size[0]:
                        recent_value = Image.fromarray(np.array(tmp_value))
                        recent_value = pytesseract.image_to_string(recent_value, lang = 'eng', config = '--psm 7 --oem 3')
                        print("Image to String: %s" % recent_value)
                        translated = translator.translate(recent_value, src='en', dest='zh-tw')
                        Mbox('translator', "\n".join([recent_value, translated.text]), 1)
                    recent_value = tmp_value
                except Exception as ex:
                    print("VALUE CHANGED EXCEPTION: %s" % recent_value)
                    # print(ex)
                    # os.system("pause")
                    recent_value = tmp_value
                    tmp_value = ""
                    pass
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