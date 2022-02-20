import subprocess
from ppadb.client import Client as AdbClient

# https://dev.to/larsonzhong/most-complete-adb-commands-4pcg#record-screen


def get_device_xy():
    cmd = r'adb shell getevent'
    w = 0
    h = 0
    try:
        p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in p1.stdout:
            line = line.decode(encoding="utf-8", errors="ignore")
            line = line.strip()
            if ' 0035 ' in line:
                e = line.split(" ")
                w = e[3]
                w = int(w, 16)  # The output is hexadecimal, therefore base 16

            if ' 0036 ' in line:
                e = line.split(" ")
                h = e[3]
                h = int(h, 16)  # Same for H as for W
                if h > 0:
                    p = (w, h)
                    print(p)
        p1.wait()

    except Exception as e:
        print(f'Failed while getting input coordinates: {e}')


def adbclient_setup():
    client = AdbClient(host="127.0.0.1", port=5037)  # Default is "127.0.0.1" and 5037

    # This section is to connect to the device wireless
    # Step 1: Turn on the server on the PC- adb start-server
    # Step 2: Set the port to 5555- adb tcpip 5555   (NOTE: Device must be connected to the laptop by USB!)
    # Step 3: The device can be disconnected now and the script can be launched
    client.remote_connect('10.240.85.7', 5555)

    devices = client.devices()  # To connect via USB
    if len(devices) == 0:
        print('No devices')
        quit()

    device = devices[0]

    print(f'Connected to {device}')

    shell_cmd = 'wm size'
    print(f'The resolution of this screen is: {device.shell(shell_cmd)}')

    #get_device_xy()     # Coordinate limit is: w:4080 and h:4095

adbclient_setup()