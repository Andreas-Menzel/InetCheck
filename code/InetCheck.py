#!/usr/bin/env python3

#-------------------------------------------------------------------------------
# InetCheck
#
# InetCheck can be used to check the systems internet connectivity. You can also
#     check if your server is still running by supplying the respective host and
#     port.
#
# https://github.com/Andreas-Menzel/InetCheck
#-------------------------------------------------------------------------------
# @author: Andreas Menzel
# @license: MIT License
# @copyright: Copyright (c) 2021 Andreas Menzel
#-------------------------------------------------------------------------------

import argparse
from signal import signal, SIGINT
import socket
import subprocess
from sys import exit
import time


# Setup parser
parser = argparse.ArgumentParser(description='Check and monitor the connectivity of a specified host.', prog='InetCheck')
parser.add_argument('--version', action='version', version='%(prog)s v1.2.1')
parser.add_argument('-H', '--host',
    metavar='',
    help='specify host')
parser.add_argument('-p', '--port',
    metavar='',
    type=int,
    help='specify port')
parser.add_argument('-t', '--timeout',
    metavar='',
    type=int,
    help='specify connection timeout')
parser.add_argument('-i', '--interval',
    metavar='',
    type=int,
    help='delay between connection checks')
parser.add_argument('-lf', '--log_file',
    metavar='',
    help='specify log file')
parser.add_argument('-cc', '--cmd_connected',
    metavar='',
    help='shell command which will be executed when the system can establish a connection to the host again')
parser.add_argument('-cd', '--cmd_disconnected',
    metavar='',
    help='shell command which will be executed when the system can not establish a connection to the host anymore')
parser.add_argument('-bc', '--beeps_connected',
    metavar='',
    type=int,
    help='number of beeps the system should make when it can establish a connection to the host again')
parser.add_argument('-bd', '--beeps_disconnected',
    metavar='',
    type=int,
    help='number of beeps the system should make when it can not establish a connection to the host anymore')
parser.add_argument('-q', '--quiet',
    action='store_true',
    help='use this to not display any output in the terminal')
args = parser.parse_args()


# Define variables and initialize with default values
conn_host = "example.com"
conn_port = 80
conn_timeout = 3

check_interval = 5
log_file = ""

cmd_connected = None
cmd_disconnected = None

beeps_connected = 0
beeps_disconnected = 0

# program variables
time_connected = 0
time_disconnected = 0


# my_print
#
# Prints text to the console if not --quiet and to a log-file if supplied.
#
# @param    string  s       String to print and save.
# @param    string  end     End.
# @param    bool    flush   Flush.
#
# @return   None
#
# @note     Use like builtin function print().
def my_print(s='', end='\n', flush=True):
    if not args.quiet:
        print(s, end=end, flush=flush)
    if log_file != "":
        file = open(log_file, 'a+')
        file.write(s + end)
        file.close()


# apply_program_arguments
#
# Get values passed to argparse and update program parameters.
#
# @return   None
def apply_program_arguments():
    global conn_host
    global conn_port
    global conn_timeout
    global check_interval
    global log_file
    global cmd_connected
    global cmd_disconnected
    global beeps_connected
    global beeps_disconnected

    if args.host != None:
        conn_host = args.host
        my_print("Using host " + conn_host)
    if args.port != None:
        conn_port = args.port
        my_print("Using port " + str(conn_port))
    if args.timeout != None:
        conn_timeout = args.timeout
        my_print("Using timeout " + str(conn_timeout) + "s")

    if args.interval != None:
        check_interval = args.interval
        my_print("Using interval " + str(check_interval) + "s")

    if args.log_file != None:
        log_file = args.log_file
        my_print("Using log-file " + log_file)

    if args.cmd_connected != None:
        cmd_connected = args.cmd_connected
        my_print("Command when connected: " + cmd_connected)
    if args.cmd_disconnected != None:
        cmd_disconnected = args.cmd_disconnected
        my_print("Command when disconnected: " + cmd_disconnected)

    if args.beeps_connected != None and args.beeps_connected >= 0:
        beeps_connected = args.beeps_connected
        my_print("Beeping " + str(beeps_connected) + " times when connected: ")
    if args.beeps_disconnected != None and args.beeps_disconnected >= 0:
        beeps_disconnected = args.beeps_disconnected
        my_print("Beeping " + str(beeps_disconnected) + " times when disconnected: ")


# check_connection
#
# Check if we can connect to a host.
#
# @param    string      host        Host.
# @param    int         port        Port.
# @param    int         timeout     Timeout.
#
# @return   Bool        Returns True if host can be reached. False otherwise.
def check_connection(host='example.com', port=80, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return False



# passed_time
#
# Convert seconds into readable string with format '0d 12h 15m 30s'.
#
# @param    int         t_seconds   The seconds to convert.
#
# @return   string      String representation of the seconds.
def passed_time(t_seconds):
    days    = int(t_seconds / (60*60*24))
    hours   = int((t_seconds - (days * (60*60*24))) / (60*60))
    minutes = int((t_seconds - (days * (60*60*24)) - hours * (60*60)) / 60)
    seconds = int(t_seconds - (days * (60*60*24)) - hours * (60*60) - minutes * (60))
    return_string = ""
    return_string += str(days) + "d "
    return_string += str(hours) + "h "
    return_string += str(minutes) + "m "
    return_string += str(seconds) + "s"
    return return_string


# time_pretty
#
# Converts a timestamp into a string with format '2022-06-15 16:17:00'.
#
# @param    number  timestamp   The timestamp to convert.
#
# @return   string  String representation of the timestamp.
def time_pretty(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


# Declare and initialize program variables
connection_status = check_connection()
connection_status_old = connection_status
time_status_change = time.time()

def main():
    global connection_status
    global connection_status_old
    global time_status_change
    global time_connected
    global time_disconnected

    global check_interval
    global log_file
    global cmd_connected
    global cmd_disconnected
    global beeps_connected
    global beeps_disconnected

    apply_program_arguments()

    # Show first connection status
    if check_connection():
        my_print("Connected     from ", end='')
    else:
        my_print("Not connected from ", end='')
    my_print(time_pretty(time_status_change), end='', flush=True)

    while True:
        # Update connection status
        connection_status_old = connection_status
        connection_status = check_connection()

        # Did connection status change?
        if connection_status and not connection_status_old:
            my_print(" to ", end='')
            my_print(time_pretty(time.time()), end='')
            my_print(" - " + passed_time(time.time() - time_status_change))
            time_disconnected += time.time() - time_status_change

            my_print("Connected     from ", end='')
            my_print(time_pretty(time_status_change), end='', flush=True)
            time_status_change = time.time()

            # Execute command and beep if requested.
            if cmd_connected != None:
                subprocess.run(cmd_connected, shell=True)
            for i in range(beeps_connected):
                print('\a', end='', flush=True)
                time.sleep(0.25)
        elif not connection_status and connection_status_old:
            my_print(" to ", end='')
            my_print(time_pretty(time.time()), end='')
            my_print(" - " + passed_time(time.time() - time_status_change))
            time_connected += time.time() - time_status_change

            my_print("Not connected from ", end='')
            my_print(time_pretty(time_status_change), end='', flush=True)
            time_status_change = time.time()

            # Execute command and beep if requested.
            if cmd_disconnected != None:
                subprocess.run(cmd_disconnected, shell=True)
            for i in range(beeps_disconnected):
                print('\a', end='', flush=True)
                time.sleep(0.25)

        time.sleep(check_interval)


# end
#
# Prints summary.
#
# @param    int         signal_received     Signal.
# @param    FrameType   frame               Frame.
#
# @return   None
def end(signal_received, frame):
    global connection_status
    global time_connected
    global time_disconnected
    global time_status_change

    if connection_status:
        time_connected += time.time() - time_status_change
    else:
        time_disconnected += time.time() - time_status_change

    my_print(" to ", end='')
    my_print(time_pretty(time.time()), end='')
    my_print(" - " + passed_time(time.time() - time_status_change))
    my_print()

    total_time = time_connected + time_disconnected

    if total_time > 0.0:
        my_print("Time connected   : " + passed_time(time_connected) + " - ", end='')
        my_print(str(round((time_connected / total_time) * 100, 2)) + "%")

        my_print("Time disconnected: " + passed_time(time_disconnected) + " - ", end='')
        my_print(str(round((time_disconnected / total_time) * 100, 2)) + "%")
    else:
        my_print("No statistics to print.")

    my_print("Goodbye!")
    exit(0)


if __name__ == "__main__":
    signal(SIGINT, end)
    main()
