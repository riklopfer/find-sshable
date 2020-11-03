Headless Raspberry Pi
======================

Start from [here](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md) to configure the WiFi on your raspberry pi. 

As per [here](https://www.raspberrypi.org/documentation/remote-access/ssh/README.md) add an empty `ssh` file to the root partition when you frist boot up. 

Locally run the following. This will find and add your Pi to the local ssh config.  

```bash
./find_pi.py
```

ssh into it, 

```bash
ssh raspberrypi
```

On there, you should [**change your password**, update locale, etc](https://www.raspberrypi.org/documentation/configuration/raspi-config.md)

```bash
sudo raspi-config
```

Also ensure that ssh runs on start up

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
``` 

