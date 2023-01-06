
# importing package
import matplotlib.pyplot as plt
import numpy as np
import sys

#print(sys.argv[1])
bench=sys.argv[1]

time_default=[]
before_default=[]
after_default=[]

beforefile_default="heap-before-" + str(bench)+"-default";
afterfile_default="heap-after-" + str(bench)+"-default";
pausefile_default=str(bench)+"-pause-default";
# Read data from file
with open(beforefile_default, 'r') as f:
    for line in f:
        if line.strip():  # skip empty lines
            before_default.append(float(line))
with open(afterfile_default, 'r') as f:
    for line in f:
        if line.strip():  # skip empty lines
            after_default.append(float(line))
with open(pausefile_default, 'r') as f:
    time_default = [float(x) for x in f]

# Plot the data
plt.plot(time_default, before_default, label="Heap Before GC")
plt.plot(time_default, after_default, label="Heap After GC")
plt.legend()
pngname="fixed soft heap-"+str(bench)+".png"
plt.savefig(pngname)
# plt.show()
  
# plot lines
# plt.plot(pause, heap, label = "line 1")
# plt.plot(heap, pause, label = "line 2")
# plt.legend()
# plt.show()