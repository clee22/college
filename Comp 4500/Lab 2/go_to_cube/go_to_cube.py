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

from find_cube import *

try:
    from PIL import ImageDraw, ImageFont
except ImportError:
    sys.exit('run `pip3 install --user Pillow numpy` to run this example')
def nothing(x):
    pass

YELLOW_LOWER = np.array([9, 115, 151])
YELLOW_UPPER = np.array([60, 255, 255])

GREEN_LOWER = np.array([8,25,13])
GREEN_UPPER = np.array([179, 254, 79])

# Define a decorator as a subclass of Annotator; displays the keypoint
class BoxAnnotator(cozmo.annotate.Annotator):

    cube = None

    def apply(self, image, scale):
        d = ImageDraw.Draw(image)
        bounds = (0, 0, image.width, image.height)

        if BoxAnnotator.cube is not None:

            #double size of bounding box to match size of rendered image
            BoxAnnotator.cube = np.multiply(BoxAnnotator.cube,2)

            #define and display bounding box with params:
            #msg.img_topLeft_x, msg.img_topLeft_y, msg.img_width, msg.img_height
            box = cozmo.util.ImageBox(BoxAnnotator.cube[0]-BoxAnnotator.cube[2]/2,
                                      BoxAnnotator.cube[1]-BoxAnnotator.cube[2]/2,
                                      BoxAnnotator.cube[2], BoxAnnotator.cube[2])
            cozmo.annotate.add_img_box_to_image(image, box, "green", text=None)

            BoxAnnotator.cube = None



async def run(robot: cozmo.robot.Robot):

    robot.world.image_annotator.annotation_enabled = True

    robot.world.image_annotator.add_annotator('box', BoxAnnotator)

    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled = True
    robot.camera.enable_auto_exposure = True

    gain,exposure,mode = 390,3,1

    # below is a singular line i added to make sure cozmo's head always starts out looking straight and not down or up
    robot.set_head_angle(cozmo.util.degrees(-10), 0.0, 2.0, 0.5, True, False, 10)

    try:

        while True:
            event = await robot.world.wait_for(cozmo.camera.EvtNewRawCameraImage, timeout=30)   #get camera image
            if event.image is not None:
                image = cv2.cvtColor(np.asarray(event.image), cv2.COLOR_BGR2RGB)

                if mode == 1:
                    robot.camera.enable_auto_exposure = True
                else:
                    robot.camera.set_manual_exposure(exposure,fixed_gain)

                #find the cube
                cube = find_cube(image, YELLOW_LOWER, YELLOW_UPPER)
                print(cube)
                BoxAnnotator.cube = cube

                ################################################################
                # Todo: Add Motion Here
                ################################################################
                if cube is None:
                    await robot.drive_wheels(-20,20)
                    justFound = True # bool for whether cube was just found or not
                    time.sleep(0.05)
                else:
                    if justFound is True:
                        robot.stop_all_motors()
                        time.sleep(1)
                        justFound = False
                        print("Found a cube")
                    elif (cube[0] < 80 and (cube[0]+cube[2]) < 240):
                        await robot.drive_wheels(30,20)
                        time.sleep(0.1)
                    elif (cube[0] > 80 and (cube[0]+cube[2]) > 240):
                        await robot.drive_wheels(20,30)
                        time.sleep(0.1)
                    elif(cube[0] < 240 and (cube[0]+cube[2]) > 80):
                        await robot.drive_wheels(30,30)
                        time.sleep(0.1)
                    elif(cube[0] < 80 and (cube[0]+cube[2]) > 240):
                        await robot.drive_wheels(0,0)
                        time.sleep(0.1)





    except KeyboardInterrupt:
        print("")
        print("Exit requested by user")
    except cozmo.RobotBusy as e:
        print(e)
    #cv2.destroyAllWindows()


if __name__ == '__main__':
    cozmo.run_program(run, use_viewer = True, force_viewer_on_top = True)
