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

just google it there are many tutorials out there

execute following commands on your PI:

`apt install wvdial`

`pip install telepot`

`ssh -R  kali-pi:22:localhost:22 serveo.net`  and type yes to permanently add the ssh key of serveo.net

### Set up wvdial and pyrat

insert your SIM into the modem and connect it to the PI


google **wvdial + your provider** to find the right configuration

open `/etc/wvdial.conf` and insert your configuration

after you set up your wvdial.conf the next step is to configure pyrat

create a **telegram bot** [click](https://api.telegram.org/bot)

open `pyrat.py` and insert your chat-id and your API-Token

`chmod +x pyrat.py` and `./pyrat.py`

pyrat automatically copies to  `/usr/bin/` 



### edit rc.local

after you edit `/etc/rc.local` it should look like this:
-----------------------------
#!/bin/sh -e
wvdial  **your config here** &
sleep 10
pyrat &
exit 0
-----------------------------

run `chmod +x /etc/rc.local`

### connect the Hardware

connect your Wifi adapter to your PI and put everything in a box.

### How to use:
after boot up the PI sends you a message via telegram

in telegram app you can type:

**/ssh** generates a command you can run on your linux-pc to connect from anywhere

**/reboot** self explaining

**/shutdown** should be used to turn the PI off   

**/help** shows a list of commands




### Demonstartion:

<a href="http://www.youtube.com/watch?feature=player_embedded&v=wne8PfzcNDQ
" target="_blank"><img src="http://img.youtube.com/vi/wne8PfzcNDQ/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>


# you can also find some pics of my build in the images Folder



























