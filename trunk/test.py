#!/usr/bin/env python
# -*- coding: UTF-8 -*

import sys, os.path

class Conf_Manager:
  # poll_time
  # file1
  # file2
  # file3 ...
  def __init__(self, pathname):
    self.pathname = pathname
    self.poll_time = 1 # default
    self.log_file_list = []

  def open(self):
    # open for reading and writing but no truncating
    f = codecs.open(self.pathname, "r+", "ascii")
    return f

  def exists(self):
    ret = (os.path.exists(self.pathname) and
    os.path.isfile(self.pathname))
    return ret

if __name__ == '__main__':
  c = Conf_Manager('/home/mano/.pylogvrc')
  print c.exists()
