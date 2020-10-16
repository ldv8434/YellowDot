import os, sys
from PIL import Image

filename = input("Please enter a filename for the image:\n")

if (os.path.exists(filename) | (filename == "")):
	print("File already exists, exiting...")
	exit()

sprite_width = int(input("Enter width of individual sprite: (default: 32)\n"))
if (sprite_width == ""):
	sprite_width = 32

sprite_height = int(input("Enter height of individual sprite: (default: 32)\n"))
if (sprite_height == ""):
	sprite_height = 32

num_wide = int(input("Enter number of sprites width-ways on a sheet: (default: 3)\n"))
if (num_wide == ""):
	num_wide = 3

num_high = int(input("Enter number of sprites height-ways on a sheet: (default: 5)\n"))
if (num_high == ""):
	num_high = 5

h_guidelines = int(input("Horizontal guidelines every (x) pixels: (default: 8; 0 to disable)"))
if (h_guidelines == ""):
	h_guidelines = 8

v_guidelines = int(input("Vertical guidelines every (x) pixels: (default: 8; 0 to disable)"))
if (v_guidelines == ""):
	v_guidelines = 8


print("Sprite size:",sprite_width,"x",sprite_height)
print("Sprites per image:",num_wide,"x",num_high)
print("Does this look correct? Y/n")
response = input().upper()
if ((response == "Y") | (response == "")):
	print()
else:
	print("Exiting...")
	exit()

width = sprite_width * num_wide
height = sprite_height * num_high


##########################
# Create new image

image = Image.new('RGBA',(width,height),(255,255,255, 0))

if (h_guidelines != 0):
	for x in range(0,width,h_guidelines):
		for y in range(height):
			image.putpixel((x,y),(255,0,0,255))

if (v_guidelines != 0):
	for y in range(0,height,v_guidelines):
		for x in range(width):
			image.putpixel((x,y),(255,0,0,255))



for x in range(0,width,sprite_width):
	for y in range(height):
		image.putpixel((x,y),(255,255,0,255))

for y in range(0,height,sprite_height):
	for x in range(width):
		image.putpixel((x,y),(255,255,0,255))
			





#########################3
# Save image
try:
	image.save(filename)
	qr_output.save("pixelpy",resolution=200)
except IOError:
	print("Cannot save")

