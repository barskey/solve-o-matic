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

-Setup kiosk mode (https://obrienlabs.net/setup-raspberry-pi-kiosk-chromium/)
- set auto-login from raspi-config
nano /home/pi/.config/autostart/kiosk.desktop
-add the following
[Desktop Entry]
Type=Application
Name=Kiosk
Exec=/home/pi/kiosk.sh
X-GNOME-Autostart-enabled=true

nano /home/pi/kiosk.sh
- add the following:
---- start kisok.sh -----
#!/bin/bash
 
# Run this script in display 0 - the monitor
export DISPLAY=:0
 
# Hide the mouse from the display
unclutter &
 
# If Chrome crashes (usually due to rebooting), clear the crash flag so we don't have the annoying warning bar
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences
 
# Run Chromium and open tabs
/usr/bin/chromium-browser --window-size=480,320 --kiosk --window-position=0,0 http://localhost:5000 &
 
# Start the kiosk loop. This keystroke changes the Chromium tab
# To have just anti-idle, use this line instead:
# xdotool keydown ctrl; xdotool keyup ctrl;
# Otherwise, the ctrl+Tab is designed to switch tabs in Chrome
# #
while (true)
 do
  xdotool keydown ctrl+Tab; xdotool keyup ctrl+Tab;
  sleep 15
done
----- end kiosk.sh -----
sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
sudo apt-get install libopenjp2-7-dev
sudo apt-get install libtiff5
sudo apt-get install python3-picamera
cd ~
git clone https://github.com/barskey/solve-o-matic.git
cd solve-o-matic
sudo apt-get install python3-venv
python3 -m pip install wheel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
