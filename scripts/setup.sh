#NOTE: RUN THIS IN ROOT OF THE PROJECT

#this is meant for raspbery pi os lite

#almost a copy of: https://github.com/riffnshred/nhl-led-scoreboard/blob/master/scripts/install.sh

sudo apt-get update
sudo apt install git python3-pip

git submodule init
git submodule update

cd submodules/rpi-rgb-led-matrix || exit
python3 -m pip install --no-cache-dir cython
python3 -m cython -2 --cplus *.pyx

make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)
