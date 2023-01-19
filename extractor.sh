#!/bin/bash

# $1 is the name of the benchmark
#echo "file: $1"
#echo "benchmark: $2"
 work="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/$2"

 
# first line for Number of GC calls (while changing soft heap size)
# second line for Number of GC calls (with fixed soft heap size)
#third line for Number of GC calls (default soft heap size behaviour)

cat $work/$1 | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk 'END{print NR}' > "$work/$1-out.txt"
cat "$work/$1-other" | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk 'END{print NR}' > "$work/$1-adoptive-out.txt"
cat "$work/$1-default" | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk 'END{print NR}' > "$work/$1-default-out.txt"

### Execution Times ###
# 90th percentileLast five execution times"
cat $work/$1 | grep "msec" | awk -F " in" '{print $2}' | awk -F " msec" '{print $1}' |  tail -n 5 | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}' >> "$work/$1-out.txt"
cat "$work/$1-other" | grep "msec" | awk -F " in" '{print $2}' | awk -F " msec" '{print $1}' |  tail -n 5 | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}' >> "$work/$1-adoptive-out.txt"
cat "$work/$1-default" | grep "msec" | awk -F " in" '{print $2}' | awk -F " msec" '{print $1}' |  tail -n 5 | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}' >> "$work/$1-default-out.txt"

### Pause Times ###
#90th percentile of all the pause times
# cat $work/$1 | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk '{print $1}' | awk -F "\\\[|s]" '{print $2}' | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}' >> "$work/$1-out.txt"
# cat "$work/$1-other" | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk '{print $1}' | awk -F "\\\[|s]" '{print $2}' | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}' >> "$work/$1-adoptive-out.txt"
# cat "$work/$1-default" | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk '{print $1}' | awk -F "\\\[|s]" '{print $2}' | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}' >> "$work/$1-default-out.txt"

### tail latency"
#90th percental of all 90th percentile taile latencies
lat=`cat $work/$1 | awk '/warmup 6/{f=1;print} f'| grep "metered tail latency" | awk -F "90%| usec" '{print $3}' | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}'`
lat_other=`cat "$work/$1-other" | awk '/warmup 6/{f=1;print} f'| grep "metered tail latency" | awk -F "90%| usec" '{print $3}' | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}'`
lat_def=`cat "$work/$1-default" | awk '/warmup 6/{f=1;print} f'| grep "metered tail latency" | awk -F "90%| usec" '{print $3}' | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}'`

if [[ -z "$lat" ]]
then
      echo "0">> "$work/$1-out.txt"
      echo "0">> "$work/$1-adoptive-out.txt" 
      echo "0">> "$work/$1-default-out.txt"
else 
      echo $lat>> "$work/$1-out.txt"
      echo $lat_other>> "$work/$1-adoptive-out.txt" 
      echo $lat_def>> "$work/$1-default-out.txt"
fi

# [[ ! -z "$lat" ]] &&  $lat>> "$work/$1-out.txt" || 0>> "$work/$1-out.txt"
# [[ ! -z "$lat_other" ]] &&  $lat-other>> "$work/$1-adoptive-out.txt" || 0>> "$work/$1-adoptive-out.txt" 
# [[ ! -z "$lat_def" ]] &&  $lat_def>> "$work/$1-default-out.txt" || 0>> "$work/$1-default-out.txt"
 

### Heap Sizes Before Garbage Collections ###
#90th percentile of all the heap sizes before GCs 
cat $work/$1 | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk -F "->" '{print $1}' | awk -F "M\\\(" '{print $1}' | awk '{print $NF}' | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}' >> "$work/$1-out.txt"
cat "$work/$1-other" | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk -F "->" '{print $1}' | awk -F "M\\\(" '{print $1}' | awk '{print $NF}'  | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}' >> "$work/$1-adoptive-out.txt"
cat "$work/$1-default" | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk -F "->" '{print $1}' | awk -F "M\\\(" '{print $1}' | awk '{print $NF}'  | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}' >> "$work/$1-default-out.txt"


### Heap Sizes After Garbage Collections ###
#90th percentile of all the heap sizes after GCs
cat $work/$1 | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk -F "->" '{print $2}' | awk -F "M" '{print $1}' | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}' >> "$work/$1-out.txt"
cat "$work/$1-other" | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk -F "->" '{print $2}' | awk -F "M" '{print $1}' | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}' >> "$work/$1-adoptive-out.txt"
cat "$work/$1-default" | awk '/warmup 6/{f=1;print} f' | grep "Garbage Collection" | grep -e "->" | awk -F "->" '{print $2}' | awk -F "M" '{print $1}' | sort -n | awk '{arr[NR]=$1} END {print arr[int(NR*0.9)]}' >> "$work/$1-default-out.txt"
