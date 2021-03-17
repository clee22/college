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
 
def handle_object_observed(evt, **kw):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
    if isinstance(evt.obj, CustomObject):
        if(evt.obj.object_type = target1_obj.object_type)
            cube1 = evt.image_box
        if(evt.obj.object_type = target2_obj.object_type)
            cube2 = evt.image_box
        


### end of stuff for handling custom objects

### stuff for handling states below

def start_transitions(arr, cube):
    newState = "left_search"
    return (newState, arr, cube)

def left_search_state_transitions(arr, cube):
    counter = 0
    while (cube is None):
        await robot.drive_wheels(-20,20)
        time.sleep(0.066)
        # if the counter reachs 10 then the robot should have been able to rotate 360 degree a good number of times
        # to avoid either moving to fast and missing the cube detection given the space between the wheels is about 
        # 56 cm and so given the idea of a circle and the circumference needed to rotate 360 degrees diameter*pi 
        # resulting in 175.929mm in circumference meaning to do a 360 turn while turning both wheels have to travel
        # about 88 mm/s to travel 360 degrees in a second divide that by 15 for the fram count and you getabout 5.86 
        # mm/s so moving a little over 3x that about a 7th of a second (0.666) means about 3.41 full rotations of 
        # looking without finding a cube. so to remedy that the robot is set to move at a random angle, whichever the 
        # robot stopped rotating in and drive forward in a random direction before beginning to rotate again
        if (counter > 10):
            await robot.drive_wheels(20,20)
            time.sleep(0.198)
            count = -1 # set it to -1 because after if conditional 1 is added to counter making the counter 0 again
        counter = counter + 1
    
    ### the moment the cube is not None and thus found by the event handler

    arr[0] = cube.Left

    return (newState, arr, cube)



async def run(robot: cozmo.robot.Robot):

    robot.world.image_annotator.annotation_enabled = True

    robot.world.image_annotator.add_annotator('box', CustomObject)

    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled = True
    robot.camera.enable_auto_exposure = True

    # Add event handlers for whenever Cozmo sees a new object
    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)
    robot.add_event_handler(cozmo.objects.EvtObjectDisappeared, handle_object_disappeared)

    # define the target cube which has the circles4 AR symbol
    target1_obj = robot.world.define_custom_cube(CustomObjectTypes.CustomType00,
                                              CustomObjectMarkers.Circles4,
                                              45,
                                              25, 25, True)
    # define the second target cube a which has the diamonds2 AR symbol
    target2_obj = robot.world.define_custom_cube(CustomObjectTypes.CustomType01,
                                              CustomObjectMarkers.Diamonds2,
                                              45,
                                              25, 25, True)

    # below is a singular line i added to make sure cozmo's head always starts out looking straight and not down or up
    robot.set_head_angle(cozmo.util.degrees(-10), 0.0, 2.0, 0.5, True, False, 10)

    cube_pos = [None, None, None, None, None] # 5 length array intended for cube positions to tell if cube is going 
    BoxAnnotator.cube = target1_obj  # set the initial cube to cube

    fsm = StateMachine()
    fsm.add_state("Start", start_transitions)
    fsm.add_state("left_search", left_search_state_transitions)
    fsm.add_state("right_search", right_search_state_transitions)
    fsm.add_state("track", track_state_transitions)
    fsm.add_state("approach", approach_state_transitions)
    fsm.add_state("exit", None, end_state=1)
    fsm.set_start("Start")
    fsm.run(cube_pos, cube1)
    cube_pos = [None, None, None, None, None] # reset the cube pos array to nulls for the second run of the fsm to find the second cube
    fsm.run(cube_pos, cube2)



if __name__ == '__main__':
    cozmo.run_program(run, use_viewer = True, force_viewer_on_top = True)
