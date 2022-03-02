#!/bin/bash

#this is meant for raspbery pi os lite

#literally a copy of: https://github.com/riffnshred/nhl-led-scoreboard/blob/master/scripts/install.sh

sudo apt-get update
sudo apt install git python3-pip

git submodule update --init --recursive
git config submodule.matrix.ignore.all

#this is the only part tha differs from riffnshred
#for some reason this is the only method that worked for me
cd submodules/matrix || exit
cd bindings/python3

make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)
