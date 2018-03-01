# THIS IS PART OF AN EXPERIMENTAL MULTIPROCESSING IMPLEMENTATION OF FlappyAI
import time
import multiprocessing
#import pyautogui


def jumpOn(sharedvar, lock):
    lock.acquire()
    sharedvar.value = True
    lock.release()


def jumpOff(sharedvar, lock):
    lock.acquire()
    sharedvar.value = False
    lock.release()


# def pyau():
#    pyautogui.click(clicks=1)
