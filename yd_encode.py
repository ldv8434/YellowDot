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
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# dots per inch
#DPI = 400
DPI = 300

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

# Define the color yellow as an RGB tuple
YELLOW = (255,255,0)
DARK_YELLOW = (30,30,0)
#YELLOW = (0,255,255)

# Filenames
CLEARTEXT_PDF = "ProcessorArchitecture.pdf"
COVERT_PDF = "covert.pdf"
DEBUG_QR_IMG = "debug_qr.png"
DEBUG_QR_PDF = "debug_qr.pdf"

# Message to encode
MESG_TO_ENCODE = "Call me Ishmael. Some years ago, never mind how long \
precisely, having little or no money in my purse, and nothing \
particular to interest me on shore..."

############
# Encoding #
############

# open "cleartext" PDF file
ct_pdf_file = open(CLEARTEXT_PDF, 'rb')
ct_pdf_pdf = PyPDF2.PdfFileReader(ct_pdf_file)
# Convert to image
ct_pdf_img = convert_from_path(CLEARTEXT_PDF, last_page=1,dpi=DPI)[0]


# Create qr code
qr_code_obj = qrcode.QRCode(
	version=QR_VER, # determines size
	error_correction=qrcode.constants.ERROR_CORRECT_H,
	box_size=1,
	border=0,
)

qr_code_obj.add_data(MESG_TO_ENCODE)
qr_code_obj.make(fit=False)

qr_code_img = qr_code_obj.make_image(fill_color="black", back_color="white")

qr_code_img.save(DEBUG_QR_IMG)
#qr_code_img.convert("1").save("debug_qr2.pdf")



# convert qr code to 1 bit image
qr_1m = qr_code_img.convert("1")

# Write QR code to image
## Full blocks for testing purposes

# create new image, transparent background
qr_output = PIL.Image.new('RGBA',(DP_wide,DP_tall),(0,0,0,0))

# for QR pixel's x value in QR code's width/height
for x_block in range(QR_SIZE):
	for y_block in range(QR_SIZE):
		x_loc = int((x_block*QR_BS)+DPI)
		y_loc = int((y_block*QR_BS)+DPI)
		
		print(x_loc)
		print(y_loc)

		
		if not (qr_1m.getpixel((x_block,y_block))):
			for x_add in range(int(mm*mm_mod)):
				for y_add in range(int(mm*mm_mod)):
					pdf_pixel = ct_pdf_img.getpixel((x_loc+x_add, y_loc+y_add))
					if not (pdf_pixel[0] < 128 and pdf_pixel[1] < 128 and pdf_pixel[2] < 128):
						qr_output.putpixel( (x_loc+x_add, y_loc+y_add), YELLOW )
					else:
						qr_output.putpixel( (x_loc+x_add, y_loc+y_add), DARK_YELLOW )
						
# save image as pdf because reportlab doesn't like PIL objects
qr_output.save("debug_qr_pdf_intermediary.png",resolution=DPI)

# create PDF of just image, "tranparent" background
c = canvas.Canvas(DEBUG_QR_PDF,pagesize=letter)
canvas_width, canvas_height = letter
c.drawImage("debug_qr_pdf_intermediary.png",0,0,width=canvas_width,height=canvas_height,mask='auto')
c.save()

# open newly made PDF for merging
qr_pdf_file = open(DEBUG_QR_PDF,'rb')
qr_pdf_pdf = PyPDF2.PdfFileReader(qr_pdf_file)

# get first page of cleartext
ct_pdf_page = ct_pdf_pdf.getPage(0)
# get output as pdf
qr_pdf_page = qr_pdf_pdf.getPage(0)

# merge pages
ct_pdf_page.mergePage(qr_pdf_page)

# make pdf writer for output
output_pdf = PyPDF2.PdfFileWriter()
# add page to writer
output_pdf.addPage(ct_pdf_page)
# open output file
output_file = open(COVERT_PDF, 'wb')
# actually write to file
output_pdf.write(output_file)

output_file.close()
qr_pdf_file.close()
ct_pdf_file.close()


exit()

# create new image
qr_invert = PIL.Image.new('RGB',(DP_wide,DP_tall),"black")


# create tick marks
for x in range(int(LP_wide)):
		qr_invert.putpixel( (int(DPI*x), 0), YELLOW )
		qr_invert.putpixel( (int(DPI*x), 1), YELLOW )
		qr_invert.putpixel( (int(DPI*x), 2), YELLOW )
		qr_invert.putpixel( (int(DPI*x), 3), YELLOW )
for y in range(LP_tall):
		qr_invert.putpixel( (0, (int(DPI*y))), YELLOW )
		qr_invert.putpixel( (1, (int(DPI*y))), YELLOW )
		qr_invert.putpixel( (2, (int(DPI*y))), YELLOW )
		qr_invert.putpixel( (3, (int(DPI*y))), YELLOW )



# for QR pixel's x value in QR code's width/height
for x_block in range(QR_SIZE):
	for y_block in range(QR_SIZE):
		print( (int((x_block*QR_BS)+(DPI*1.5))))
		print(int((y_block*QR_BS)+(DPI*1.5)))

		
		if (qr_1m.getpixel((x_block,y_block))):
			for x_add in range(int(mm*mm_mod)):
				for y_add in range(int(mm*mm_mod)):
					qr_invert.putpixel( (int((x_block*QR_BS)+(DPI*1))+x_add, int((y_block*QR_BS)+(DPI*1))+y_add), YELLOW )


qr_invert.save("qr_invert.pdf",resolution=DPI)






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

