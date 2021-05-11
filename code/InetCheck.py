import socket
import time

# Check the internet connection
def checkConnection(host="google.de", port=80, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return False


# Declare and initialize variables
connection_status = checkConnection()
connection_status_old = connection_status
time_status_change = time.time()

# Show first connection status
if checkConnection():
    print("Connected     from ", end='')
else:
    print("Not connected from ", end='')
print(time_status_change, end='', flush=True)

while True:
    # Update connection status
    connection_status_old = connection_status
    connection_status = checkConnection()

    # Did connection status change?
    if connection_status and not connection_status_old:
        print(" to ", end='')
        print(time.time())
        print("Connected     from ", end='')
        print(time_status_change, end='', flush=True)
        time_status_change = time.time()
    elif not connection_status and connection_status_old:
        print(" to ", end='')
        print(time.time())
        print("Not connected from ", end='')
        print(time_status_change, end='', flush=True)
        time_status_change = time.time()

    time.sleep(1)
