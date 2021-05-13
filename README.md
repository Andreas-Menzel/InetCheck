# InetCheck

A simple Python script that checks the system's internet connection.


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
