#! /usr/bin/env python
# -*- coding: UTF-8 -*

import pygtk
pygtk.require('2.0')

import gobject
import gtk.gdk
import gtk
if gtk.pygtk_version < (2,3,90):
  print "PyGtk 2.3.90 or later required for this example"
  raise SystemExit

import gtk.glade
import re
import codecs
import sys
import os
import signal
import _fam
import time
from threading import Thread
from threading import Event

class Conf_Manager:
  def __init__(self):
    print "uh"

class File_Monitor(Thread):
  def __init__(self, parent, pathname, poll_time, event):
    self.suspend = None
    self.cont = None
    self.intr = None
    self.usr1 = None
    self.usr2 = None

    self.event = event

    Thread.__init__(self)
    self.parent = parent
    self.pathname = pathname
    self.poll_time = poll_time
    self.fam_conn = _fam.open()
    self.request = self.fam_conn.monitorFile(self.pathname, None)
    
    signal.signal(signal.SIGTSTP, self.handle_stop)
    signal.signal(signal.SIGCONT, self.handle_cont)
    signal.signal(signal.SIGINT, self.handle_int)
    signal.signal(signal.SIGUSR1, self.handle_usr1)
    signal.signal(signal.SIGUSR2, self.handle_usr2)

  def handle_stop(self, signum, frame):
      print 'Suspended!'
      self.suspend = 1

  def handle_cont(self, signum, frame):
      print 'Resumed!'
      signal.signal(signal.SIGCONT, self.handle_cont)
      self.cont = 1

  def handle_int(self, signum, frame):
      print 'Interupted!'
      signal.signal(signal.SIGINT, self.handle_int)
      self.intr = 1

  def handle_usr1(self, signum, frame):
      print 'Got USR1!'
      signal.signal(signal.SIGUSR1, self.handle_usr1)
      self.usr1 = 1

  def handle_usr2(self, signum, frame):
      print 'Got USR2!'
      signal.signal(signal.SIGUSR2, self.handle_usr2)
      self.usr2 = 1

  def run(self):
    while True:
      # event set means main window closed
      if self.event.isSet():
        sys.exit(0)

      if self.suspend:
        self.fam_conn.suspendMonitor()
        
      if self.cont:
        self.fam_conn.resumeMonitor()
      
      if self.intr:
        sys.exit(0)
      
      time.sleep(self.poll_time)
      
      while self.fam_conn.pending():
        event = self.fam_conn.nextEvent()
        print event.filename, event.code2str()

# TODO: USER OS.PATH.GETMTIME() !!!
# TODO: use os.open and os.fstat to monitor log file access times
# TODO: and os.ST_ATIME, os.ST_MTIME and os.ST_CTIME in particular
# TODO:
# TODO: use time module to get current time -- perhaps time.time() and
# TODO: convert from fstat to long format and compare

class PyLogV:
  def start_file_monitor(self, pathname):
    fm = File_Monitor(self, pathname, 0.6, self.event)
    #fm.start()
    return fm

  def add_text(self, text):
    self.text_buffer.insert_at_cursor(text)
    
  def open_file(self, filename):
    f = codecs.open(filename, "r", "ascii")
    return f
  
  def get_text_from_file(self, f):
    return f.read()
  
  def preferences_delete_event(self, widget, event, data=None):
    self.preferences.hide()
    return gtk.TRUE

  def delete_event(self, widget, event, data=None):
    # If you return FALSE in the "delete_event" signal handler,
    # GTK will emit the "destroy" signal. Returning TRUE means
    # you don't want the window to be destroyed.
    # This is useful for popping up 'are you sure you want to quit?'
    # type dialogs.
    
    # Change TRUE to FALSE and the main window will be destroyed with
    # a "delete_event".

    self.event.set()
    # gnome/metacity doesn't like this with such a great poll time :S
    for key, value in self.file_monitors.iteritems():
      print "Waiting for '" + key + "' file monitor to stop"
      value.join()
    return gtk.FALSE

  def destroy(self, widget, data=None):
    #print "destroy event ocurred"
    gtk.main_quit()
   
  def show_preferences(self, event):
    self.preferences.show()

  def create_filechooser(self):
    dialog = gtk.FileChooserDialog("Open..",
                                   None,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)

    filter = gtk.FileFilter()
    filter.set_name("All files")
    filter.add_pattern("*")
    dialog.add_filter(filter)

    return dialog

  def show_filechooser(self, event):
    fc = self.create_filechooser()
    response = fc.run()
    
    if response == gtk.RESPONSE_OK:
      self.filename = fc.get_filename()
    elif response == gtk.RESPONSE_CANCEL:
      print 'closed, nothing selected'
    fc.destroy()

    self.add_log_file_to_log_files(self.filename)

  def add_log_file_to_log_files(self, log_file):
    self.estupido = self.estupido + 1
    self.log_files_model.append([self.estupido, log_file])

  def __init__(self, log_file_list):
    # parse the glade file
    self.all_widgets = gtk.glade.XML("pylogv.glade")
    self.parvo = 1
    self.estupido = 1
    
    # save the log_file_list if present in args
    self.log_file_list = log_file_list
    # get the widgets
    # window stuff
    self.main_window = self.all_widgets.get_widget("mainwindow")
    self.main_window.connect("delete_event", self.delete_event)
    self.main_window.connect("destroy", self.destroy)

    self.preferencias_menu_item = self.all_widgets.get_widget("preferencias")
    self.preferencias_menu_item.connect("activate", self.show_preferences)
    self.preferencias_toolbar_item = self.all_widgets.get_widget("toolbutton1")
    self.preferencias_toolbar_item.connect("clicked", self.show_preferences)
    self.quit_menu_item = self.all_widgets.get_widget("sair1")
    self.quit_menu_item.connect("activate", self.destroy)

    self.add_button = self.all_widgets.get_widget("add")
    self.remove_button = self.all_widgets.get_widget("remove")
    self.browse_button = self.all_widgets.get_widget("browse")
    self.browse_button.connect("clicked", self.show_filechooser)
    # end window stuff

    self.preferences = self.all_widgets.get_widget("preferences")
    self.preferences.hide()
    self.preferences.connect("delete_event", self.preferences_delete_event)
    
    self.text_view = self.all_widgets.get_widget("textview")
    self.text_buffer = self.text_view.get_buffer()
    
    #self.show_logs = self.all_widgets.get_widget("show_logs")
    #self.show_logs_model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING)
    #self.show_logs.set_model(self.show_logs_model)
    #renderer2 = gtk.CellRendererText()
    #column2 = gtk.TreeViewColumn("logs", renderer2, text=1)
    #self.show_logs.append_column(column2)

    self.entry = self.all_widgets.get_widget("entry")
    
    self.log_files = self.all_widgets.get_widget("log_files")

    self.log_files_model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING)
    self.log_files.set_model(self.log_files_model)

    # add the files passed to monitor list
    for file in self.log_file_list:
      self.add_log_file_to_log_files(file)
    
    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn("log_files", renderer, text=1)
    self.log_files.append_column(column)
    
    f = self.open_file("/var/log/errors")
    self.add_text(self.get_text_from_file(f))

    # setup communication with file monitor
    self.event = Event()
    
    # setup file monitors assoc array
    self.file_monitors = {}

    for value in self.log_file_list:
      self.file_monitors[value] = self.start_file_monitor(value)
      self.file_monitors[value].start()

    #self.file_monitors['/home/mano/teste.fam'] = self.start_file_monitor('/home/mano/teste.fam')
    #self.file_monitors['/home/mano/teste.fam'].start()
      
if __name__ == '__main__':
  gtk.gdk.threads_init()
  list = sys.argv[1:]
# create the window
  window = PyLogV(list)

  gtk.gdk.threads_enter()
  gtk.main()
  gtk.gdk.threads_leave()
