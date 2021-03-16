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
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes

try:
    from PIL import ImageDraw, ImageFont
except ImportError:
    sys.exit('run `pip3 install --user Pillow numpy` to run this example')
def nothing(x):
    pass

### stuff for custom object handling below
 
def handle_object_appeared(evt, **kw):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
    if isinstance(evt.obj, CustomObject):
        print("Cozmo started seeing a %s" % str(evt.obj.object_type))


def handle_object_disappeared(evt, **kw):
    # This will be called whenever an EvtObjectDisappeared is dispatched -
    # whenever an Object goes out of view.
    if isinstance(evt.obj, CustomObject):
        print("Cozmo stopped seeing a %s" % str(evt.obj.object_type))

def custom_objects(robot: cozmo.robot.Robot):
    # Add event handlers for whenever Cozmo sees a new object
    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)
    robot.add_event_handler(cozmo.objects.EvtObjectDisappeared, handle_object_disappeared)

    # define the target cube which has the circles4 AR symbol
    target_obj = robot.world.define_custom_cube(CustomObjectTypes.CustomType00,
                                              CustomObjectMarkers.Circles4,
                                              45,
                                              25, 25, True)
    # define the non importan/tracked cube as a distraction and has the diamonds2 AR symbol
    distractor_obj = robot.world.define_custom_cube(CustomObjectTypes.CustomType01,
                                              CustomObjectMarkers.Diamonds2,
                                              45,
                                              25, 25, True)

### end of stuff for handling custom objects

### stuff for handling states below

def start_transitions(txt):
    cube_pos = [None, None, None, None, None] # 5 length array intended for cube positions to tell if cube is going 
    newState = "left_search"
    return (newState, cube_pos)

def left_search_state_transitions(txt):
    
    while (target_obj is None):
        await robot.drive_wheels(-20,20)
        time.sleep(0.05)
    
    

    return (newState, cube_pos)



async def run(robot: cozmo.robot.Robot):

    # below is a singular line i added to make sure cozmo's head always starts out looking straight and not down or up
    robot.set_head_angle(cozmo.util.degrees(-10), 0.0, 2.0, 0.5, True, False, 10)

    fsm = StateMachine()
    fsm.add_state("Start", start_transitions)
    fsm.add_state("left_search", left_search_state_transitions)
    fsm.add_state("right_search", right_search_state_transitions)
    fsm.add_state("track", track_state_transitions)
    fsm.add_state("approach", approach_state_transitions)
    fsm.add_state("exit", None, end_state=1)
    fsm.set_start("Start")
    fsm.run()


if __name__ == '__main__':
    cozmo.run_program(run, use_viewer = True, force_viewer_on_top = True)
