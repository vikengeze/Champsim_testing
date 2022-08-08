#!/bin/bash

echo "Building no prefetcher"
./build_champsim.sh bimodal no no no no lru 1 no
echo "Done"

echo "Building sequential prefetcher"
./build_champsim.sh bimodal no no no no lru 1 sp > /dev/null 2>&1
echo "Done"

echo "Building arbitrary stride prefetcher"
./build_champsim.sh bimodal no no no no lru 1 asp > /dev/null 2>&1
echo "Done"

echo "Building distance prefetcher"
./build_champsim.sh bimodal no no no no lru 1 dp > /dev/null 2>&1
echo "Done"

echo "Building simple from file prefetcher(to use as oracle)"
./build_champsim.sh bimodal no no no no lru 1 from_file > /dev/null 2>&1
echo "Done"

notify-send "Building is done"
