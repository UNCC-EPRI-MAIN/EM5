import os

os.system("git clone --recursive https://github.com/dusty-nv/jetson-inference ~/jetson-inference")

os.system("sudo mkdir ~/jetson-inference/python/training/classification/data/Model1_BlockedPath/")
os.system("sudo cp labels.txt ~/jetson-inference/python/training/classification/data/Model1_BlockedPath/")

os.system("sudo mkdir ~/jetson-inference/python/training/classification/models/blocked/")
os.system("sudo cp resnet18.onnx ~/jetson-inference/python/training/classification/models/blocked/")
os.system("sudo cp Camera.py ~/jetson-inference/python/training/classification/")
os.system("sudo cp -f run.sh ~/jetson-inference/docker/")

print("To run the container, you must run the command 'cd ~/jetson-inference' and then 'docker/run.sh'")
print("In the container, run the python script at 'python/training/classification/Camera.py'")