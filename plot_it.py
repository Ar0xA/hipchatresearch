import numpy as np
import matplotlib.pyplot as plt
import sys


def readdata(filename):
    #alright, lets read the values 
    #we read it like this, because of how plt wants the results
    with open(filename, 'r') as f:
        x_axisValues=f.readline().strip().replace(",","")
        y_axisValues=f.readline().strip()

    #some funky magic, since plt wants tuples from integers, not strings
    tmp_tuple=(y_axisValues).split(',')
    y_tuple=()
    for nums in tmp_tuple:
        y_tuple=y_tuple+(int(nums),)
    return y_tuple

#lets first read our initial x axis (from the first file)
with open("result_0.csv", 'r') as f:
    x_axisValues=f.readline().strip().replace(",","")

#we set the length of the x_axis the amount of values
#so no cut off
ind = np.arange(len(x_axisValues))
width = 0.35

#we do this to draw the rectangles
fix, ax= plt.subplots()
rects2 = ax.bar(ind,readdata(sys.argv[1]), width, color='red')

ax.set_xticks(ind+width)
ax.set_xticklabels( tuple(x_axisValues) )
ax.set_title(sys.argv[1])
plt.show()
