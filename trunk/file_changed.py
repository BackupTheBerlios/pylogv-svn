#! /usr/bin/env python
# -*- coding: UTF-8 -*

import os, os.path, time, sys, threading

def modified(self, monitor_start_time, file_mtime):
  return file_mtime <= monitor_start_time

class File_Monitor:
  def thread_callback(self, args):
    fmtime = os.path.getmtime(self.pathname)
    
    if modified(self.monitor_start_time, fmtime):
      # protected code
      self.lock.acquire()
      self.modified = True
      self.lock.release()
      # end protected code
    else:
      time.sleep(self.polling_interval)

  def is_modified(self):
    return self.modified

  def set_polling_interval(self, poll_interval):
    self.polling_interval = poll_interval

  def get_polling_interval(self):
    return self.polling_interval

  def __init__(self, pathname, monitor_start_time, polling_interval):
    self.modified = False
    self.polling_interval = polling_interval
    self.monitor_start_time = monitor_start_time
    self.lock = thread.allocate_lock()
    self.pathname = pathname
    self.thread = thread.start_new_thread(self.thread_callback,()) # function, args (tuple)

if __name__ == '__main__':
  fm = File_Monitor('/var/log/kernel', time.time(), 1)
#pathname = None
#if len(sys.argv) == 2:
#  pathname = sys.argv[1]
#
#now = time.time()
#fd = os.path.getmtime(pathname)
#print "tempo agora %d" % now
#print "tempo ultimo de modificacao de " + pathname + " = " + str(fd)
#print "modificado no passado? " + str(fd < now)
