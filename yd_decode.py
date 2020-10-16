#######################################
#
#	Yellow Dot - Python Script 
#	Author: Lukas Vacula
#
#
#######################################


import os, sys
import PIL
from pdf2image import convert_from_path, convert_from_bytes
import qrcode
from pyzbar.pyzbar import decode
import PyPDF2

# dots per inch
#DPI = 200
DPI = 600

# 1mm side definition
mm = int(DPI // 25.4)

# size of dots in mm
mm_mod = 0.25

# letter paper size
LP_wide = 8.5
LP_tall = 11

# dots wide and tall minus borders
DP_wide = int(LP_wide * DPI)
DP_tall = int(LP_tall * DPI)

# QR version stuffs
QR_VER = 14
QR_SIZE = 17 + (QR_VER*4)

# Size of QR "block"/pixel in image
# 1 inch margins on all sides (DPI*2)
# QR_SIZE+1 to give wiggle room
QR_BS = (DP_wide-(DPI*2)) // (QR_SIZE+1)

# Offset for search range
QR_BS_OFFSET = int(QR_BS // 2)

# Define limits for colors
# value must be greater than
RED = 240
GREEN = 240
DARK_RED = 25
DARK_GREEN = 25
# value must be less than
BLUE = 220
DARK_BLUE = 15

RGB = (255,0,0)

# Filenames
# pdf containing covert channel
COVERT_PDF = "scanned3.pdf"
OUTPUT_FILE = "scanned3.png"


############
# Encoding #
############

# open "cleartext" PDF file
pdf_file = open(COVERT_PDF, 'rb')
pdf_pdf = PyPDF2.PdfFileReader(pdf_file)

# Convert to image
pdf_img = convert_from_path(COVERT_PDF,last_page=1,dpi=DPI)[0]
pdf_img = pdf_img.convert("RGB")


# top left corner
tl_corner = (0,0)
# top right corner
tr_corner = (0,0)
# bottom left corner
bl_corner = (0,0)

found_corner = False
# search from corner inward 
# if this isn't already a searching algo, it should be
for dist in range(0, DP_wide):
	for var in range(dist):
		this_pixel = pdf_img.getpixel((var, dist-var))
		if (this_pixel[0] > RED and this_pixel[1] > GREEN and this_pixel[2] < BLUE):
			tl_corner = (var, dist-var)
			found_corner = True
			break
	if (found_corner):
		break


found_corner = False
# same for top right
for dist in range(1, DP_wide):
	for var in range(1, dist):
		this_pixel = pdf_img.getpixel((DP_wide-var, dist-var))
		# check to see if this is the corner yellow dot
		if (this_pixel[0] > RED and this_pixel[1] > GREEN and this_pixel[2] < BLUE):
			tr_corner = (DP_wide-var, dist-var)
			found_corner = True
			break
	if (found_corner):
		break


found_corner = False
# same for bottom left
for dist in range(1, DP_wide):
	for var in range(1, dist):
		print((var, DP_wide-(dist-var)))
		this_pixel = pdf_img.getpixel((var, DP_wide-(dist-var)))
		# check to see if this is the corner yellow dot
		if (this_pixel[0] > RED and this_pixel[1] > GREEN and this_pixel[2] < BLUE):
			bl_corner = (var, DP_wide-(dist-var))
			found_corner = True
			break
	if (found_corner):
		break

print("tl_corner", tl_corner)
print("tr_corner", tr_corner)
print("bl_corner", bl_corner)

# get slope of y change from left to right
y_incline_adjust = (tl_corner[1]-tr_corner[1])/(tl_corner[0]-tr_corner[0])
# get slope of x change from top
x_incline_adjust = (tl_corner[0]-bl_corner[0])/(tl_corner[1]-bl_corner[1])


print(x_incline_adjust)
print(y_incline_adjust)

# create new image for output, 4px border
qr_output = PIL.Image.new('1',(QR_SIZE+8,QR_SIZE+8),1)


# create new block sizes based on minima and maxima
x_bs = (tr_corner[0] - tl_corner[0]) / (QR_SIZE-1)
y_bs = (bl_corner[1] - tl_corner[1]) / (QR_SIZE-1)

# for QR pixel's x value in QR code's width/height
# search from top left's X value to top right's X value
for x_block in range(QR_SIZE):
	# search from top left's Y value to bottom left's Y value
	for y_block in range(QR_SIZE):
		# Get "center point" to search from
		# adjust for X based on Y
		x_loc = int((x_block*x_bs)+tl_corner[0]+(x_incline_adjust*y_block))
		# adjust for Y based on X
		y_loc = int((y_block*y_bs)+tl_corner[1]+(y_incline_adjust*x_block))
		
		#print("x_loc", x_loc)
		#print("y_loc", y_loc)

		i = 0
		# scan range of detected dots
		
		has_dot = False
		for x_add in range(QR_BS_OFFSET*2):
			for y_add in range(QR_BS_OFFSET*2):
				i += 1
				#print("location", (x_loc+x_add-QR_BS_OFFSET,y_loc+y_add-QR_BS_OFFSET))
				this_pixel = pdf_img.getpixel((x_loc+x_add-QR_BS_OFFSET,y_loc+y_add-QR_BS_OFFSET))
				#print(this_pixel)
				
				if (this_pixel[0] > RED and this_pixel[1] > GREEN and this_pixel[2] < BLUE):
					pdf_img.putpixel((x_loc+x_add-QR_BS_OFFSET,y_loc+y_add-QR_BS_OFFSET), RGB)
					qr_output.putpixel((x_block+4,y_block+4), 0)
					has_dot = True
					break
				
				
				elif (False):# (this_pixel[0] > DARK_RED and this_pixel[1] > DARK_GREEN and this_pixel[2] < DARK_BLUE) :
				
				#if ((this_pixel[0] + this_pixel[1]) / 2 > (this_pixel[2] + 20)):
				
					pdf_img.putpixel((x_loc+x_add-QR_BS_OFFSET,y_loc+y_add-QR_BS_OFFSET), RGB)
					qr_output.putpixel((x_block+4,y_block+4), 0)
					has_dot = True
					break
			if (has_dot):
				break
				
				# MAX: location (2840, 2827)

				
		#print(i)	
					#qr_output.putpixel( (int((x_block*QR_BS)+(DPI*1))+x_add, int((y_block*QR_BS)+(DPI*1))+y_add), YELLOW )

#qr_output = PIL.ImageOps.invert(qr_output)
qr_output.save(OUTPUT_FILE,resolution=DPI)

#pdf_img.save("debug_output.pdf",resolution=DPI)

print(decode(qr_output)[0].data.decode("utf-8"))

exit()
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
except IOError:
	print("Cannot save")

