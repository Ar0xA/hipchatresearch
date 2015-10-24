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
width = 0.11

#we do this to draw the rectangles
fix, ax= plt.subplots()
#rects1 = ax.bar(ind,readdata("result_0.csv"), width, color='r')
rects2 = ax.bar(ind,readdata("result_1.csv"), width, color='green')
rects3 = ax.bar(ind+width,readdata("result_2.csv"), width, color='yellow')
rects4 = ax.bar(ind+(width*2),readdata("result_3.csv"), width, color='blue')
rects5 = ax.bar(ind+(width*3),readdata("result_4.csv"), width, color='orange')
rects6 = ax.bar(ind+(width*4),readdata("result_5.csv"), width, color='purple')
rects7 = ax.bar(ind+(width*5),readdata("result_6.csv"), width, color='cyan')
rects8 = ax.bar(ind+(width*6),readdata("result_7.csv"), width, color='magenta')

print x_axisValues
#newVal=""
#for items in x_axisValues:
#    newVal=newVal+items + "    "    
#print newVal
#exit(1)
ax.set_xticks(ind+width)
ax.set_xticklabels( tuple(x_axisValues) )
#ax.set_xticklabels( tuple(newVal) )
ax.set_title("resultset")
ax.legend((rects2[0], rects3[0]), ("pos1","pos2"))
plt.show()
