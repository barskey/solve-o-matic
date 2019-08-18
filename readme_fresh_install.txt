-Steps to take for fresh install:
-Install raspberry pi stretch to sd card using balenaEtcher
-Configure network, name, enable ssh, camera, spi, i2c(?)
sudo raspi-config
-For 3.5in touch screen
sudo apt-get install cmake
cd ~
git clone https://github.com/waveshare/LCD-show.git
sudo ./LCD35-show
- to fix inverted x axis (may need to also edit line in /boot/config/txt to dtoverlay=waveshare35a,swapxy=1)
sudo apt-get install xserver-xorg-input-evdev
sudo cp -rf /usr/share/X11/xorg.conf.d/10-evdev.conf /usr/share/X11/xorg.conf.d/45-evdev.conf
sudo reboot

-Setup kiosk mode (https://pimylifeup.com/raspberry-pi-kiosk/)

sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
sudo apt-get install libopenjp2-7-dev
sudo apt-get install libtiff5
sudo apt-get install python3-picamera
sudo apt install libatlas3-base
cd ~
git clone https://github.com/barskey/solve-o-matic.git
cd solve-o-matic
sudo apt-get install python3-venv
python3 -m pip install wheel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
