#!/usr/bin/env python3
#!c:/Python35/python3.exe -u
import asyncio
import sys
import cv2
import numpy as np
import cozmo
import time
import os
from glob import glob

from statemachine import *

try:
    from PIL import ImageDraw, ImageFont
except ImportError:
    sys.exit('run `pip3 install --user Pillow numpy` to run this example')
def nothing(x):
    pass

def start_transitions(txt):
    cube_pos = [None, None, None, None, None] # 5 length array intended for cube positions to tell if cube is going 
    newState = "left_search"
    return (newState, cube_pos)

def left_search_state_transitions(txt):
    
    

    return (newState, cube_pos)



async def run(robot: cozmo.robot.Robot):

    m = StateMachine()
    m.add_state("Start", start_transitions)
    m.add_state("left_search", left_search_state_transitions)
    m.add_state("right_search", right_search_state_transitions)
    m.add_state("track", track_state_transitions)
    m.add_state("approach", approach_state_transitions)
    m.add_state("exit", None, end_state=1)
    m.set_start("Start")
    m.run()


if __name__ == '__main__':
    cozmo.run_program(run, use_viewer = True, force_viewer_on_top = True)
