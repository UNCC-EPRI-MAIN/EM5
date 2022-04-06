import os

os.system("git clone --recursive https://github.com/dusty-nv/jetson-inference ~/jetson-inference")

os.system("sudo mkdir ~/jetson-inference/python/training/classification/data/Model1_BlockedPath/")
os.system("sudo cp -f labels.txt ~/jetson-inference/python/training/classification/data/Model1_BlockedPath/")

os.system("sudo mkdir ~/jetson-inference/python/training/classification/models/blocked/")
os.system("sudo cp -f resnet18.onnx ~/jetson-inference/python/training/classification/models/blocked/")
os.system("sudo cp -f Camera.py ~/jetson-inference/python/training/classification/")
os.system("sudo cp -f run.sh ~/jetson-inference/docker/")

print("")
print("")
print("To run the container, you must run the command 'cd ~/jetson-inference' and then 'docker/run.sh'")
print("In the container, first install serial with the command 'pip3 install pyserial'")
print("then run 'cd python/training/classification/'")
print("To run the model, run the python script by 'python3 Camera.py' in the container")
print("")
print("")