#!/bin/bash

# $1 is the name of the benchmark
echo "Benchmark: $1"
echo "For the last 5 itteartions:"

### Execution Times ###
echo "Last five execution times (when changing soft heap size):"
cat $1 | grep "msec" | awk -F "in" '{print $2}' | awk -F " msec" '{print $1}' |  tail -n 5 
echo "90th percentile of all the execution times (when changing soft heap size) is: `cat $1 | grep "msec" | awk -F "in" '{print $2}' | awk -F " msec" '{print $1}' |  tail -n 5 | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}'`"

echo "Last five execution times (with default soft heap size):"
cat "$1-default" | grep "msec" | awk -F "in" '{print $2}' | awk -F " msec" '{print $1}' |  tail -n 5 
echo "90th percentile of all the execution times (with default soft heap size) is: `cat "$1-default" | grep "msec" | awk -F "in" '{print $2}' | awk -F " msec" '{print $1}' |  tail -n 5 | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}'`"

### Pause Times ###
cat $1 | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk '{print $1}' | awk -F "\\\[|s]" '{print $2}' > $1-pause
echo "90th percentile of all the pause times (when changing soft heap size) is: `cat "$1-pause" | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}'`"

cat "$1-default" | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk '{print $1}' | awk -F "\\\[|s]" '{print $2}' > $1-pause-default
echo "90th percentile of all the pause times (with default soft heap size) is: `cat "$1-pause-default" | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}'`"

### Heap Sizes Before Garbage Collections ###
cat $1 | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk -F "->" '{print $1}' | awk -F "M\\\(" '{print $1}' | awk '{print $NF}' > heap-before-$1
cat "$1-default" | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk -F "->" '{print $1}' | awk -F "M\\\(" '{print $1}' | awk '{print $NF}' > heap-before-$1-default

echo "90th percentile of all the heap sizes before GCs (when changing soft heap size) is: `sort -n heap-before-$1 | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}'`" 
echo "90th percentile of all the heap sizes before GCs (with default soft heap size) is: `sort -n heap-before-$1-default | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}'`" 

### Heap Sizes After Garbage Collections ###
cat $1 | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk -F "->" '{print $2}' | awk -F "M" '{print $1}' > heap-after-$1
cat "$1-default" | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk -F "->" '{print $2}' | awk -F "M" '{print $1}' > heap-after-$1-default

echo "90th percentile of all the heap sizes after GCs (when changing soft heap size) is: `sort -n heap-after-$1 | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}'`" 
echo "90th percentile of all the heap sizes after GCs (with default soft heap size) is: `sort -n heap-after-$1-default | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}'`" 

python3 not-fixed-soft-heap-chart.py $1
python3 fixed-soft-heap-chart.py $1
rm heap-before-$1 heap-before-$1-default heap-after-$1 heap-after-$1-default $1-pause $1-pause-default