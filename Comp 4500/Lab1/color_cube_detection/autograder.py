from count_cubes import *
import numpy as np
from glob import glob

datapath = 'data/'

ground_truth = np.genfromtxt(datapath + 'ground_truth.csv', delimiter=',', dtype='int')
answer = dict([(item[0],(item[1], item[2])) for item in ground_truth])

y_score = 0
g_score = 0

imgs = [f for f in glob(datapath+'*') if '.jpg' in f]

for f in imgs:
    i = int(f[-6:-4])
    img = cv2.imread(f,-1)

    num_yellow, num_green = count_cubes(img)

    if num_yellow == answer[i][0]: 
        y_score += 1
    else:
        print(i)
    if num_green == answer[i][1]:
        g_score += 1
    else:
        print(i)

print("Yellow Score: {}/{}".format(y_score, len(imgs)))
print("Green Score: {}/{}".format(g_score, len(imgs)))