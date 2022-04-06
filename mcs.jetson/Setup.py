import os

if not os.path.isdir("~/jetson-inference"):
    os.system("git clone --recursive https://github.com/dusty-nv/jetson-inference ~/")

os.system("sudo mkdir ~/jetson-inference/python/training/classification/data/Model1_BlockedPath/")
os.system("sudo cp labels.txt ~/jetson-inference/python/training/classification/data/Model1_BlockedPath/")

os.system("sudo mkdir ~/jetson-inference/python/training/classification/models/blocked/")
os.system("sudo cp resnet18.onnx ~/jetson-inference/python/training/classification/models/blocked/")
os.system("sudo cp Camera.py ~/jetson-inference/python")

os.system("cd ~/jetson-inference")
os.system("docker/run.sh")