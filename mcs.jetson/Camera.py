import jetson.inference
import jetson.utils
import serial
#For more information on the imageNet API:
#https://rawgit.com/dusty-nv/jetson-inference/python/docs/html/python/jetson.inference.html#imageNet

uart = serial.Serial("/dev/ttyTHS1", baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE, timeout=10.00)

net = jetson.inference.imageNet(argv=['--model=/models/blocked/resnet18.onnx', '--labels=data/Model1_BlockedPath/labels.txt'])
input = jetson.utils.videoSource("/dev/video0")
output = jetson.utils.videoOutput("display://0:")
font = jetson.utils.cudaFont()

while True:
	# capture the next image
	img = input.Capture()

	# classify the image
	class_id, confidence = net.Classify(img)

	# find the object description
	class_desc = net.GetClassDesc(class_id)

	# Needed only if wanting to display live video feed
	# # overlay the result on the image	
	# font.OverlayText(img, img.width, img.height, "{:05.2f}% {:s}".format(confidence * 100, class_desc), 5, 5, font.White, font.Gray40)
	
	# # render the image
	# output.Render(img)

	# # update the title bar
	# output.SetStatus("{:s} | Network {:.0f} FPS".format(net.GetNetworkName(), net.GetNetworkFPS()))

	# # print out performance info
	# net.PrintProfilerTimes()
	message = class_desc + '/n'
	uart.write(message.encode())

	# exit on input/output EOS
	if not input.IsStreaming() or not output.IsStreaming():
		break


