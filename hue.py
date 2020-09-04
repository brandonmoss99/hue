from phue import Bridge
import sys

#connect to bridge
b = Bridge('192.168.1.202')
b.connect()
b.get_api()

#get all the lights
#lights = b.lights
#for l in lights:
#	print(l.name)

if int(sys.argv[2]) < 0 or int(sys.argv[2]) > 255:
	print('Brightness must be between 0 and 255!')
else:
	if sys.argv[1] == "kitchen":
		b.set_light(['Kitchen 1', 'Kitchen 2', 'Kitchen 3', 'Kitchen 4'], 'bri', int(sys.argv[2]))