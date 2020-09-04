from phue import Bridge
import sys, getopt

room = None
brightness = None
on = None

argv = sys.argv[1:]

#try getting supported parameters and args from command line
try:
	opts, args = getopt.getopt(argv, "r:b:of", ["room=", "brightness=", "on", "off", "help"])
except:
	print("Error parsing options")

#assign variables based on command line parameters and args
for opt, arg in opts:
	if opt in ['-r', '--room']:
		room = arg
	elif opt in ['-b', '--brightness']:
		#try converting brightness argument to integer type
		try:
			brightness = int(arg)
		except:
			print("Error converting brightness to an integer!")
	elif opt in ['-o', '--on']:
		on = 1
	elif opt in ['-f', '--off']:
		on = 0
	elif opt in ['--help']:
		print("\nList of Parameters:\n\n(r)oom to control [room]\nTurn lights (o)n\nTurn lights of(f)\n(b)rightness of lights [0-255]")

#connect to bridge
b = Bridge('192.168.1.202')
b.connect()
b.get_api()

#check if lights should be turned on/off
if on == 1:
	if room == "kitchen":
		print("Turning on",room,"lights")
		b.set_light(['Kitchen 1', 'Kitchen 2', 'Kitchen 3', 'Kitchen 4'], 'on', True)
elif on == 0:
	if room == "kitchen":
		print("Turning off",room,"lights")
		b.set_light(['Kitchen 1', 'Kitchen 2', 'Kitchen 3', 'Kitchen 4'], 'on', False)

#check if a brightness was given to change light brightness
if brightness is not None:
	#brightness value sanity check
	if brightness < 0 or brightness > 255:
		print('Brightness must be between 0 and 255!')
	else:
		if room == "kitchen":
			print("Setting",room,"lights to brightness level",brightness)
			b.set_light(['Kitchen 1', 'Kitchen 2', 'Kitchen 3', 'Kitchen 4'], 'bri', brightness)