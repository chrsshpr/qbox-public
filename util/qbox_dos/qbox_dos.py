#!/usr/bin/python
# qbox_dos.py: extract dos from Qbox output
# generate dos plot in gnuplot format
# use: qbox_dos.py emin emax width file.r
# the DOS is accumulated separately for each spin

import xml.sax
import sys
import math

if len(sys.argv) != 5:
  print "use: ",sys.argv[0]," emin emax width file.r"
  sys.exit()

emin = float(sys.argv[1])
emax = float(sys.argv[2])
width = float(sys.argv[3])
infile = sys.argv[4]

ndos = 501
de = (emax - emin)/(ndos-1)

# normalized gaussian distribution in one dimension
# f(x) = 1/(sqrt(pi)*width) * exp(-(x/width)^2 )
def gauss(x, width):
  return (1.0/(math.sqrt(math.pi)*width)) * math.exp(-(x/width)**2)
  
# Qbox output handler to extract and process data
class QboxOutputHandler(xml.sax.handler.ContentHandler):
  def __init__(self):
    self.nspin = 1
    self.readData = 0
    self.dos_up = [0] * ndos
    self.dos_dn = [0] * ndos

  def startElement(self, name, attributes):
    if name == "eigenvalues":
      self.n = attributes["n"]
      self.spin = int(attributes["spin"])
      self.kpoint = attributes["kpoint"]
      self.weight = float(attributes["weight"])
      self.readData = 1
      self.buffer = ""
      if self.spin == 1:
        self.nspin = 2

  def characters(self, data):
    if self.readData:
      self.buffer += data

  def endElement(self, name):
    if name == "eigenvalues":
      self.readData = 0
      self.accumulate_dos()

  def accumulate_dos(self):
    self.e = self.buffer.split()
    if self.spin == 0:
      for i in range(len(self.e)):
        for j in range(ndos):
          ej = emin + j * de
          self.dos_up[j] += gauss(float(self.e[i])-ej, width ) * self.weight
    if self.spin == 1:
      for i in range(len(self.e)):
        for j in range(ndos):
          ej = emin + j * de
          self.dos_dn[j] += gauss(float(self.e[i])-ej, width ) * self.weight

  def print_dos(self):
    print "# ",infile," spin=0 width=",width
    for j in range(ndos):
      ej = emin + j * de
      print ej, self.dos_up[j]
    if self.nspin == 2:
      print
      print
      print "# ",infile," spin=1 width=",width
      for j in range(ndos):
        ej = emin + j * de
        print ej, self.dos_dn[j]

parser = xml.sax.make_parser()
handler = QboxOutputHandler()
parser.setContentHandler(handler)
parser.parse(infile)
handler.print_dos()
