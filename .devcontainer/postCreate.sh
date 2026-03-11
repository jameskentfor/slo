#!/bin/bash
set -e

sudo chown -R "$(whoami)" /workspace
sudo apt-get update && sudo apt-get install -y liblo-tools
pip3 install -r sonify/requirements.txt
