#!/usr/bin/env python
# -*- coding: UTF-8 -*

import sys, os.path, codecs

class Conf_Manager:
  # poll_time
  # file1
  # file2
  # file3 ...
  def __init__(self, pathname):
    self.pathname = pathname
    self.poll_time = 1 # default
    self.log_file_list = []
    
    if self.exists():
      self.fd = self.open()
    else:
      self.create()

  def create(self):
    # file does not exist
    self.fd = codecs.open(self.pathname, 'w+', 'ascii')
    self.write_default()
    
  def close(self):
    self.fd.close()

  def write_default(self):
    self.add_line('poll_time=1')

  def open(self):
    # open for reading and writing but no truncating
    self.fd = codecs.open(self.pathname, 'r+', 'ascii')

  def read_lines(self):
    return self.fd.readlines()

  def add_line(self, line):
    self.fd.write(line)

  def exists(self):
    ret = (os.path.exists(self.pathname) and
    os.path.isfile(self.pathname))
    return ret
  
  def set_poll_time(self, poll_time):
    self.poll_time = poll_time

if __name__ == '__main__':
  c = Conf_Manager('/home/mano/.pylogvrc')
