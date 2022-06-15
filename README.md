# InetCheck

InetCheck can be used to check the systems internet connectivity. You can also
check if your server is still running by supplying the respective host and port.


## Usage

```shell
usage: InetCheck.py [-h] [-H] [-p] [-t] [-i] [-lf] [-cc] [-cd] [-bc] [-bd]

Check and monitor the internet connection

optional arguments:
  -h, --help            show this help message and exit
  -H , --host           specify host
  -p , --port           specify port
  -t , --timeout        specify connection timeout
  -i , --interval       delay between connection checks
  -lf , --log_file      specify log file
  -cc , --cmd_connected
                        shell command which will be executed when the system
                        can establish a connection to the host again
  -cd , --cmd_disconnected
                        shell command which will be executed when the system
                        can not establish a connection to the host anymore
  -bc , --beeps_connected
                        number of beeps the system should make when it can
                        establish a connection to the host again
  -bd , --beeps_disconnected
                        number of beeps the system should make when it can not
                        establish a connection to the host anymore
```


## Examples

### Simple logging to file

```
./InetCheck.py --log_file 'Connection.log'
```

### Logging with status-change notification

Play beep-sound 3x when reconnected and 5x when disconnected.

```
./InetCheck.py --log_file 'Connection.log' -bc 3 -bd 5
```

### Check if server is running

Check if host example.com can be reached.
```
./InetCheck.py --log_file 'Connection.log' --host 'example.com'
```
