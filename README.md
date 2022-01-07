Find SSH-able
=============
[![Python application](https://github.com/riklopfer/find-sshable/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/riklopfer/find-sshable/actions/workflows/python-app.yml)

Find SSH-able devices on your network and (optionally) add them to you ssh config in a cleanish way. Tested locally with MacOS and runs with Actions on Ubuntu. 

Setup
=====

1. Install [nmap](https://nmap.org)
    
    MacOS

    ```bash
    brew install nmap
    ```

    Debian 

    ```shell
    sudo apt-get install nmap
    ```

2. (optional / recommended) create a python virtual env and activate it. 
3. pip isntall 

    ```shell
    pip install find-sshable
    ```
4. Run the program

    ```shell
    find-sshable --help
    ```

Testing
=======

```shell
# pip install pytest
PYTHONPATH=. pytest -vs .
```

Headless Raspberry Pi
======================

The idea is to stand up a headless raspberry pi that you can ssh into and do things on.

If you will run this on Wifi (not ethernet), start
from [here](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md) to configure the WiFi on your
raspberry pi. However, if you can connect to ethernet, I would recommend doing so, and you can skip this step.

As per [here](https://www.raspberrypi.org/documentation/remote-access/ssh/README.md) add an empty `ssh` file to the root
partition when you frist boot up.

Locally run the following. This will find and add your Pi to the local ssh config.

```bash
find_sshable --host-pattern "raspberrypi" --update-ssh-config --ssh-user "pi"
```

        scanning for devices... 00:15

        Found 2 devices...
        Host(name='raspberrypi.lan', ip=IPv4Address('192.168.86.20'))
        Host(name='raspberrypi.lan', ip=IPv4Address('192.168.86.36'))

        Devices will be added to your ssh config as follows
        find-sshable.raspberrypi.lan-0    192.168.86.20
        find-sshable.raspberrypi.lan-1    192.168.86.36

ssh into it,

```bash
ssh find-sshable.raspberrypi.lan-0
```

On there, you should [**change your
password**, update locale, etc](https://www.raspberrypi.org/documentation/configuration/raspi-config.md)

```bash
sudo raspi-config
```

Also ensure that ssh runs on start up

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
``` 

