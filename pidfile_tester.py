#!/usr/bin/env python3

# MIT License

# Copyright (c) 2018 vnetman@zoho.com

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ------------------------------------------------------------------------------

"""Program to demonstrate/test the pidfile module

This program has two modes of operation:

- In the "run" mode, it uses the pidfile module to make an entry for its PID in
  the /var/run/user/<uid>/pidfilester.pid file, then enters an infinite loop out
  of which it exits on the receipt of SIGUSR1

- In the "kill" mode, it uses the pidfile module to read the PID of the most
  recently started "run" instance, and sends a SIGUSR1 to that process.

The demo/test involves starting one or more instances of this program in the
"run" mode, then running it in the "kill" mode to terminate the most recently
started "run" instance.
"""

import os
import sys
import argparse
import time
import signal
from pidfile import PidFile

PROGRAM_NAME = 'pidfiletester'

STOP_RECORDING = False

def sigusr1_handler(sig, frm):
    global STOP_RECORDING
    STOP_RECORDING = True

def run():
    signal.signal(signal.SIGUSR1, sigusr1_handler)
    p = PidFile(PROGRAM_NAME)  ## <----
    p.sanitize_pid_file()      ## <----
    added = p.add()            ## <----

    odd = False
    while True:
        if STOP_RECORDING:
            p.remove()         ## <----
            sys.exit(0)
            break # Unreachable, added just for readability

        time.sleep(3)

        if odd:
            odd = False
            print('{}'.format(added), end='', flush=True)
        else:
            odd = True
            print('>', end='', flush=True)

def kill():
    p = PidFile(PROGRAM_NAME)     ## <----
    p.sanitize_pid_file()         ## <----
    pid_last_instance = p.last()
    if not pid_last_instance:
        print('No running instances of ' + PROGRAM_NAME)
        return
    print('Killing {}'.format(pid_last_instance))
    os.kill(pid_last_instance, signal.SIGUSR1)
    time.sleep(4)
    pid_last_instance = p.last()  ## <----
    if not pid_last_instance:
        print('Killed, no more running instances of ' + PROGRAM_NAME)
    else:
        print('Killed, last instance is now {}'.format(pid_last_instance))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser_group = parser.add_mutually_exclusive_group(required=True)
    parser_group.add_argument('--run', action='store_true')
    parser_group.add_argument('--kill', action='store_true')
    args = parser.parse_args()

    if args.run:
        run()
    elif args.kill:
        kill()
    else:
        raise ValueError('Neither \'--run\' nor \'--kill\' specified.')
