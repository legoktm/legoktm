#!/usr/bin/python3

import timetest, montyhall, sys

start = timetest.start()
m = montyhall.MontyHall()
m.gameshow(int(sys.argv[1]))
timetest.end(start)
