
# importing package
import matplotlib.pyplot as plt
import numpy as np
import sys

#print(sys.argv[1])
bench=sys.argv[1]

time=[]
time_default=[]
before=[]
after=[]
before_default=[]
after_default=[]

beforefile_default="heap-before-" + str(bench)+"-default";
beforefile="heap-before-" + str(bench);
afterfile_default="heap-after-" + str(bench)+"-default";
afterfile="heap-after-" + str(bench);
pausefile=str(bench)+"-pause";
pausefile_default=str(bench)+"-pause-default";
# Read data from file
with open(beforefile, 'r') as f:
    for line in f:
        if line.strip():  # skip empty lines
            before.append(float(line))
with open(afterfile, 'r') as f:
    for line in f:
        if line.strip():  # skip empty lines
            after.append(float(line))
with open(pausefile, 'r') as f:
    time = [float(x) for x in f]

# Plot the data
plt.plot(time, before, label="Heap Before GC")
plt.plot(time, after, label="Heap After GC")
plt.legend()
pngname="not-fixed soft heap-"+str(bench)+".png"
plt.savefig(pngname)
# plt.show()
  
# plot lines
# plt.plot(pause, heap, label = "line 1")
# plt.plot(heap, pause, label = "line 2")
# plt.legend()
# plt.show()