# THIS IS PART OF AN EXPERIMENTAL MULTIPROCESSING IMPLEMENTATION OF FlappyAI

import multiprocessing
import numpy as np
import FlapDebugScript as fd
import FlappyBird as fb
import BirdBrains as bb
import time


def FlappyBird(sharedTele, sharedJump, lock):
    fb.FlappyBird(sharedTele, sharedJump, lock).run()


def FlapDebug(sharedJump, lock):
    time.sleep(.25)
    for i in range(25):
        fd.jumpOn(sharedJump, lock)
        time.sleep(.03)
        fd.jumpOff(sharedJump, lock)
        time.sleep(.405)


def RunNeuralNet(sharedTele, sharedJump, lock):
    bird = bb.BirdBrain()
    for i in range(500):
        flap = bird.forward(
            np.array([[sharedTele.value[0], sharedTele.value[1]]]))
        if flap > 0.4:
            fd.jumpOn(sharedJump, lock)
            time.sleep(.03)
            fd.jumpOff(sharedJump, lock)
            time.sleep(.305)


if __name__ == '__main__':

    globalTelemetry = multiprocessing.Manager().Namespace()
    globalJump = multiprocessing.Value('b', False)
    lock = multiprocessing.Lock()

    FlappyBirdSubprocess = multiprocessing.Process(
        target=FlappyBird, args=(globalTelemetry, globalJump, lock))

    # BirdBrainSubprocess = multiprocessing.Process(
    #   target=RunNeuralNet, args=(globalTelemetry, globalJump, lock))

    # FlapDebugSubprocess = multiprocessing.Process(
    #    target=FlapDebug, args=(globalJump, lock))

    FlappyBirdSubprocess.start()
    time.sleep(1.0)
    # BirdBrainSubprocess.start()
    # FlapDebugSubprocess.start()

    while FlappyBirdSubprocess.is_alive():
        print(globalTelemetry.value)

    FlappyBirdSubprocess.join()
    # BirdBrainSubprocess.join()
    # FlapDebugSubprocess.join()
