import argparse
from signal import signal, SIGINT
import socket
import subprocess
from sys import exit
import time


# Setup parser
parser = argparse.ArgumentParser(description='Check and monitor the internet connection')
parser.add_argument('-H', '--host', help='unknown')
parser.add_argument('-p', '--port', type=int, help='unknown')
parser.add_argument('-t', '--timeout', type=int, help='unknown')
parser.add_argument('-i', '--interval', type=int, help='unknown')
parser.add_argument('-lf', '--log_file', help='unknown')
parser.add_argument('-cc', '--cmd_connected', help='unknown')
parser.add_argument('-cd', '--cmd_disconnected', help='unknown')
parser.add_argument('-bc', '--beeps_connected', type=int, help='unknown')
parser.add_argument('-bd', '--beeps_disconnected', type=int, help='unknown')
args = parser.parse_args()


# Define variables and initialize with default values
conn_host = "example.com"
conn_port = 80
conn_timeout = 3

check_interval = 5
log_file = None

cmd_connected = None
cmd_disconnected = None

beeps_connected = 0
beeps_disconnected = 0


# Update variables according to program parameters
if args.host != None:
    conn_host = args.host
    print("Using host " + conn_host)
if args.port != None:
    conn_port = args.port
    print("Using port " + conn_port)
if args.timeout != None:
    conn_timeout = args.timeout
    print("Using timeout " + conn_timeout + "s")

if args.interval != None:
    check_interval = args.interval
    print("Using interval " + check_interval + "s")

if args.log_file != None:
    log_file = args.log_file
    print("Using log-file " + log_file)

if args.cmd_connected != None:
    cmd_connected = args.cmd_connected
    print("Command when connected: " + cmd_connected)
if args.cmd_disconnected != None:
    cmd_disconnected = args.cmd_disconnected
    print("Command when disconnected: " + cmd_disconnected)

if args.beeps_connected != None and args.beeps_connected >= 0:
    beeps_connected = args.beeps_connected
    print("Beeping " + str(beeps_connected) + " times when connected: ")
if args.beeps_disconnected != None and args.beeps_disconnected >= 0:
    beeps_disconnected = args.beeps_disconnected
    print("Beeping " + str(beeps_disconnected) + " times when disconnected: ")


# Check the internet connection
def check_connection(host=conn_host, port=conn_port, timeout=conn_timeout):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return False


# Convert seconds into readable string
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


def time_pretty(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


# Declare and initialize variables
connection_status = check_connection()
connection_status_old = connection_status
time_status_change = time.time()


# Show first connection status
if check_connection():
    print("Connected     from ", end='')
else:
    print("Not connected from ", end='')
print(time_pretty(time_status_change), end='', flush=True)


def main():
    global connection_status
    global connection_status_old
    global time_status_change
    while True:
        # Update connection status
        connection_status_old = connection_status
        connection_status = check_connection()

        # Did connection status change?
        if connection_status and not connection_status_old:
            print(" to ", end='')
            print(time_pretty(time.time()), end='')
            print(" - " + passed_time(time.time() - time_status_change))
            print("Connected     from ", end='')
            print(time_pretty(time_status_change), end='', flush=True)
            time_status_change = time.time()

            if cmd_connected != None:
                subprocess.run(cmd_connected)
            for i in range(beeps_connected):
                print('\a', end='', flush=True)
                time.sleep(0.25)
        elif not connection_status and connection_status_old:
            print(" to ", end='')
            print(time_pretty(time.time()), end='')
            print(" - " + passed_time(time.time() - time_status_change))
            print("Not connected from ", end='')
            print(time_pretty(time_status_change), end='', flush=True)
            time_status_change = time.time()

            if cmd_disconnected != None:
                subprocess.run(cmd_disconnected)
            for i in range(beeps_disconnected):
                print('\a', end='', flush=True)
                time.sleep(0.25)

        time.sleep(check_interval)


def end(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


if __name__ == "__main__":
    signal(SIGINT, end)
    main()
