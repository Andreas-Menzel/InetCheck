import socket
import time

def checkInternetSocket(host="google.de", port=80, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return False


connection_status = "NOT SET"
connection_status_old = "NOT SET"
time_status_change = time.time()

print("", end='')

while True:
    connection_status_old = connection_status
    connection_status = checkInternetSocket()

    if connection_status:
        if not connection_status_old:
            print(" to ", end='')
            print(time.time())
            print("Connected     from ", end='')
            print(time_status_change, end='', flush=True)
            time_status_change = time.time()
    else:
        if connection_status_old:
            print(" to ", end='')
            print(time.time())
            print("Not connected from ", end='')
            print(time_status_change, end='', flush=True)
            time_status_change = time.time()

    time.sleep(1)
