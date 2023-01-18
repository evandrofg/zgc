#!/bin/bash
work="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

for overhead in 0.5 1 2 5 10 15 20
do
    for bench in  avrora lusearch #tomcat jme h2 avrora batik biojava eclipse fop graphchi luindex pmd  sunflow xalan zxing #h2o jython spring tradebeans tradesoap 
    do
        sudo bash ./extractor.sh "$bench-$overhead" "$bench"
        python3 excel.py $bench $overhead
        rm -r "$work/$bench/$bench-$overhead-out.txt"
        rm -r "$work/$bench/$bench-$overhead-default-out.txt"
        rm -r "$work/$bench/$bench-$overhead-adoptive-out.txt"
    done
done

## cassandra incompatible with java 20
#h20 Only Java versions 8-15 are supported
#jython Checksum failure
#spring failed
#tradesoap , tradebeen no data