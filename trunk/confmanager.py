#!/usr/bin/env python
# -*- coding: UTF-8 -*

import sys, os.path, codecs, re
#from xml.dom import minidom

class Conf_Manager:
  def __init__(self, pathname, default=None):
    self.pathname = pathname
    if default == None:
      self.default = """poll_time=1
file=/var/log/errors/
file=/var/log/messages"""
    else:
      self.default = default

    if self.exists():
      self.open()
    else:
      self.create()

    file = self.read()
    if re.search('poll', file):
      print 'matxxx'
    #self.prog = re.compile(self.read())
    #print '[' + self.read() + ']'
    #print re.search('poll', self.read())

  def create(self):
    # file does not exist
    self.fd = codecs.open(self.pathname, 'w+b')
    self.write_default()
    
  def close(self):
    self.fd.close()

  def write_default(self):
    self.add_text(self.default)

  def open(self):
    # open for reading and writing but no truncating
    self.fd = codecs.open(self.pathname, 'r+b')

  def read_lines(self):
    return self.fd.readlines()
    #for line in self.fd.readlines():
    #  print '[' + line + ']'

  def read(self):
    return self.fd.read()

  def add_text(self, text):
    self.fd.write(text)

  def add_line(self, line):
    self.fd.write(line)

  def exists(self):
    ret = (os.path.exists(self.pathname) and
    os.path.isfile(self.pathname))
    return ret

if __name__ == '__main__':
  c = Conf_Manager('/home/mano/.pylogvrc')
