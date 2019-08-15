Steps to take for fresh install:
Install raspberry pi stretch lite to sd card using balenaEtcher
Configure network, name, enable ssh, camera, spi, i2c(?)
sudo raspi-config
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install git
** For 3.5in touch screen
sudo apt-get install cmake
git clone https://github.com/waveshare/LCD-show.git
cd LCD-show
sudo ./LCD35-show

sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
cd ~
git clone https://github.com/barskey/solve-o-matic.git
cd solve-o-matic
sudo apt --fix-broken install
sudo apt-get install python3-pip
sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt