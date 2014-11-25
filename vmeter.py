#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is an example of a simple sound capture script
# with text vmeter.
##
# The script opens an ALSA pcm for sound capture. Set
# various attributes of the capture, and reads in a loop,
# Then prints a vmeter with curses.
##
# To test it out, run it and shout at your microphone:

import alsaaudio
import time
import audioop
import curses

# Open the device in nonblocking capture mode. The last argument could
# just as well have been zero for blocking mode. Then we could have
# left out the sleep call in the bottom of the loop
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)

# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# The period size controls the internal number of frames per period.
# The significance of this parameter is documented in the ALSA api.
# For our purposes, it is suficcient to know that reads from the device
# will return this many frames. Each frame being 2 bytes long.
# This means that the reads below will return either 320 bytes of data
# or 0 bytes of data. The latter is possible because we are in nonblocking
# mode.
inp.setperiodsize(160)


def main():
    curses.wrapper(loop)


def loop(screen):

    screen.nodelay(1)   # avoid getch() blocking wait
    screen.keypad(1)

    while True:
        # Read key pressed
        event = screen.getch()
        if event == ord("q"):
            break

        # Read data from device
        l, data = inp.read()

        if l:
            # Return the maximum of the absolute value of
            # all samples in a fragment.
            level = audioop.max(data, 2)
            screen.clear()
            screen.addstr(0, level // 200 - 2, str(level))
            screen.addstr(1, 0, level // 200 * '*')
            screen.refresh()

        time.sleep(.01)


if __name__ == '__main__':
    main()
