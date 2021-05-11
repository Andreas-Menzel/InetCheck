import socket
import time

# Check the internet connection
def check_connection(host="google.de", port=80, timeout=3):
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
    elif not connection_status and connection_status_old:
        print(" to ", end='')
        print(time_pretty(time.time()), end='')
        print(" - " + passed_time(time.time() - time_status_change))
        print("Not connected from ", end='')
        print(time_pretty(time_status_change), end='', flush=True)
        time_status_change = time.time()

    time.sleep(1)
