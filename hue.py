from phue import Bridge
import sys, getopt

ip = None
light = None
room = None
brightness = None
colour = None
colourTemp = None
saturation = None
on = None

#map light types to integer
lightTypes = {"Dimmable light":"0", "Color temperature light":"1", "Extended color light":"2"}

#hardcoded tuples of lights in each room
roomLights = {"kitchen":('Kitchen 1', 'Kitchen 2', 'Kitchen 3', 'Kitchen 4'),
	"bedroom": ('Bedroom 1', 'Bedroom 2', 'Bedroom 3', 'Bedroom 4', 'Bedroom Lamp'),
	"office": ('Office 1', 'Office 2', 'Office 3', 'Office 4', 'Office 5', 'Office 6')}

def getHelp():
	print("\nList of Parameters:\n\n"+
		"(l)ight to control [\'light\']\n"+
		"(r)oom to control [room]\n"+
		"Turn lights (o)n\n"+
		"Turn lights of(f)\n"+
		"(b)rightness of lights [0-255]\n"+
		"(c)olour of lights [0-65535]\n"+
		"colour (t)empature of lights [154-500] or [2000-6500] for Kelvin\n"+
		"(s)aturation of light colour [0-255]\n")

#get light capabilities
def getCapabilities(light):
	lightType = int(lightTypes[b.get_light(light, 'type')])
	return lightType

#get lowest light capability in a room
def getRoomCapabilities(room):
	lowestLightType = 0
	for light in roomLights[room]:
		lightType = int(lightTypes[b.get_light(light, 'type')])
		if min(lightType, lowestLightType) == lightType:
			lowestLightType = lightType
	return lowestLightType


#change the light
def modifyLight(light, lightType, brightness, colour, colourTemp, saturation, on):
	#change light on/off
	if on == 1:
		print("Turning on",light,"light")
		b.set_light(light, 'on', True)
	elif on == 0:
		print("Turning off",light,"light")
		b.set_light(light, 'on', False)

	#change light brightness
	if brightness is not None:
		#brightness value sanity check
		if brightness < 0 or brightness > 255:
			print('Brightness must be between 0 and 255!')
		else:
			print("Setting",light,"light to brightness value",brightness)
			b.set_light(light, 'bri', brightness)

	#change light saturation
	if saturation is not None:
		if saturation < 0 or saturation > 255:
			print('Saturation must be between 0 and 255!')
		else:
			if lightType == 2:
				print("Setting",light,"light to saturation value",saturation)
				b.set_light(light, 'sat', saturation)
			else:
				print("Light is incapable of saturation changing! Not changing saturation")

	#change light colour temperature
	if colourTemp is not None:
		if colourTemp not in range (154,501) and colourTemp not in range (2000,6501):
			print('Colour temperature must be between 154 and 500 or 2000-6500K!')
		else:
			if lightType in [1,2]:
				if colourTemp in range (154,501):
					print("Setting",light,"light to colour temperature value",colourTemp)
					b.set_light(light, 'ct', colourTemp)
				elif colourTemp in range(2000,6501):
					print("Setting",light,"light to colour temperature value",colourTemp,"kelvin")
					b.set_light(light, 'ct', int(1000000/colourTemp))
			else:
				print("Light is incapable of colour temperature changing! Not changing colour temperature")

	#change light colour
	if colour is not None:
		if colour < 0 or colour > 65535:
			print('Colour must be between 0 and 65535!')
		else:
			if lightType == 2:
				print("Setting",light,"light to colour value",colour)
				b.set_light(light, 'hue', colour)
			else:
				print("Light is incapable of colour changing! Not changing colour")


argv = sys.argv[1:]

#try getting supported parameters and args from command line
try:
	opts, args = getopt.getopt(argv, "i:l:r:b:c:t:s:of", ["ip=", "light=", "room=", "brightness=", "colour", "temperature", "saturation", "on", "off", "help"])
except:
	print("Error parsing options")
	getHelp()
	sys.exit(2)

#assign variables based on command line parameters and args
for opt, arg in opts:
	if opt in ['-i', '--ip']:
		ip = arg
	if opt in ['-l', '--light']:
		light = arg
	if opt in ['-r', '--room']:
		room = arg
	elif opt in ['-b', '--brightness']:
		#try converting brightness argument to integer type
		try:
			brightness = int(arg)
		except:
			print("Error converting brightness to an integer!")

	elif opt in ['-c', '--colour']:
		try:
			colour = int(arg)
		except:
			print("Error converting colour to an integer!")

	elif opt in ['-t', '--temperature']:
		try:
			colourTemp = int(arg)
		except:
			print("Error converting colour temperature to an integer!")

	elif opt in ['-s', '--saturation']:
		try:
			saturation = int(arg)
		except:
			print("Error converting saturation to an integer!")

	elif opt in ['-o', '--on']:
		on = 1
	elif opt in ['-f', '--off']:
		on = 0
	elif opt in ['--help']:
		getHelp()

#connect to bridge
if ip is not None:
	b = Bridge(ip)
	b.connect()
	b.get_api()
else:
	print('ip address for hue bridge not input!')

if(light is not None):
	modifyLight(light,getCapabilities(light), brightness, colour, colourTemp, saturation, on)

if(room is not None):
	lowestLightType = getRoomCapabilities(room)
	for light in roomLights[room]:
		modifyLight(light,lowestLightType, brightness, colour, colourTemp, saturation, on)
