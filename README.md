# pwnbox
Hack Wifi anywhere with a Raspberry Pi and a HSUPA Modem

# Getting Started:
## things you need:
1.) **Raspberry Pi 2 or 3 + 16GB+ microSD-card**

2.) **HSUPA/HSDPA Modem and a SIM card**   [I used this one](https://www.amazon.de/gp/product/B01J9C7NE0/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1)

3.) A **Wifi Adapter** capable of **Monitor-Mode & Packet injection** [I used this one](https://www.amazon.de/gp/product/B01D064VMS/ref=oh_aui_detailpage_o04_s01?ie=UTF8&psc=1)

4.) a Power Bank

5.) a Box to mount everything


## Setting it up:
First set up the PI. I recommend to use **Sticky-Fingers-Kali-Pi** for this project.
### Important:
**ssh needs to be enabled before login**


execute following commands on your PI:

`apt install wvdial`

`pip install telepot`

`ssh -R  kalilinux:22:localhost:22 serveo.net`  and type yes to permanently add the ssh key of serveo.net









