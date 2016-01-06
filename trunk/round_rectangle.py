from PIL import Image, ImageDraw

def round_corner(radius, fill):
	corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
	draw = ImageDraw.Draw(corner)
	draw.pieslice((0, 0, radius*2, radius*2), 180, 270, fill=fill)
	return corner

def round_rectangle(size, radius, fill, corners=[1, 1, 1, 1]):
	width, height = size
	rectangle = Image.new('RGBA', size, fill)
	corner = round_corner(radius, fill)
	if corners[0]:
		rectangle.paste(corner, (0, 0))
	if corners[3]:
		rectangle.paste(corner.rotate(90), (0, height-radius))
	if corners[2]:
		rectangle.paste(corner.rotate(180), (width-radius, height-radius))
	if corners[1]:
		rectangle.paste(corner.rotate(270), (width-radius, 0))
	return rectangle
