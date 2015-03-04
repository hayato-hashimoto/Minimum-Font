#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse;
from PIL import Image
from os.path import splitext
from os.path import basename

numchars = []

def init_numchars():
    for col in range(0, 16):
      pattern = []
      for y in range(0, height):
        bit = 0
        for x in range(0, width):
          color = img_rgb.getpixel(((col + 1) * width + x, height + y))
          bit += (color == (0, 0, 0)) << x
        pattern.append(bit)
      numchars.append(pattern)

def read_point(page):
  ret = 0
  for col in range(0, 16):
    pattern = []
    for y in range(0, height):
      bit = 0
      for x in range(0, width):
        color = img_rgb.getpixel(((page * 18 + col) * width + x, y))
        bit += (color == (0, 0, 0)) << x
      pattern.append(bit)
    found = False
    for i in range(0, 16):
      if (numchars[i] == pattern):
        ret = ret * 16 + i
        found = True
    if (not found):
     return ret

parser = argparse.ArgumentParser(description='Convert an image to a BDF font.')
parser.add_argument('filename')
parser.add_argument('width', type=int)
parser.add_argument('height', type=int)
args = parser.parse_args()
filename = args.filename
width = args.width
height = args.height
xheight = 4
yheight = 6
print ("""STARTFONT 2.1
FONT -mf-""" + splitext(basename(filename))[0] + '-Medium-R-Normal--' + format(height) + """-110-96-96-C-139-ISO10646-1
SIZE 11 96 96
FONTBOUNDINGBOX """ + format(height) + ' ' + format(height) + """ 0 -2
STARTPROPERTIES 24
FAMILY_NAME""" + "\"" + splitext(basename(filename))[0] + "\"" + """
FOUNDRY "mf"
SETWIDTH_NAME "Normal"
ADD_STYLE_NAME ""
WEIGHT_NAME "Medium"
SLANT "R"
PIXEL_SIZE """ + format(height) + """
RASTERIZER_VERSION 140
RESOLUTION_X 96
RESOLUTION_Y 96
SPACING "C"
AVERAGE_WIDTH 80
CHARSET_REGISTRY "ISO10646"
CHARSET_ENCODING "1"
MIN_SPACE """ + format(width) + """
WEIGHT 10
RESOLUTION 99
X_HEIGHT """ + format(xheight) + """
QUAD_WIDTH """ + format(width) + """
POINT_SIZE 110
FONT_ASCENT """ + format (height - yheight + xheight) + """
FONT_DESCENT """ + format(yheight - xheight) + """
ENDPROPERTIES""")
print ("CHARS " + format(16 * 6 * 3))
img = Image.open(filename)
img_rgb =  img.convert("RGB")
init_numchars()
for page in range(0, 3):
  start = read_point(page)
  for row in range(0, 6):
    for col in range(0, 16):
      print ("STARTCHAR U+" + format(start + 16 * row + col, "04X"))
      print ("ENCODING " + format(start + 16 * row + col))
      print ("SWIDTH 500 0")
      print ("DWIDTH " + format(width) + " 0")
      print ("BBX " + format(width) + " " + format(height) + " 0 " + format(-yheight + xheight))
      print ("BITMAP")
      for y in range(0, height):
        bits = []
        nbits = 0
        for x in range(0, width):
          color = img_rgb.getpixel(((page * 18 + col + 1) * width + x, (row + 2) * height + y))
          # print ((" ", ":")[(color == (0, 0, 0))], end="");
          bits.append((color == (0, 0, 0)))
          nbits += 1
        for i in range(0, 1 + int(nbits / 8)):
          out = 0
          for j in range(0, 8):
            if (i * 8 + j < nbits):
              out = (out << 1) + bits[i* 8 + j]
            else:
              out = (out << 1)
          print(format(out, "02X"))
      print ("ENDCHAR")
print("ENDFONT")
