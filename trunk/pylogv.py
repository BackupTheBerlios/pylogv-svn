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
import _fam
import time
from threading import Thread

class File_Monitor(Thread):
  def __init__(self, parent, pathname, poll_time):
    Thread.__init__(self)
    self.parent = parent
    self.pathname = pathname
    self.poll_time = poll_time
    self.fam_conn = _fam.open()
    self.request = self.fam_conn.monitorFile(self.pathname, None)

  def handle_stop(signum, frame):
      global suspend
      
      print 'Suspended!'
      suspend = 1

  def handle_cont(signum, frame):
      global cont
      
      print 'Resumed!'
      signal.signal(signal.SIGCONT, handle_cont)
      cont = 1

  def handle_int(signum, frame):
      global intr
      
      print 'Interupted!'
      signal.signal(signal.SIGINT, handle_int)
      intr = 1

  def handle_usr1(signum, frame):
      global usr1
      
      print 'Got USR1!'
      signal.signal(signal.SIGUSR1, handle_usr1)
      usr1 = 1

  def handle_usr2(signum, frame):
      global usr2
      
      print 'Got USR2!'
      signal.signal(signal.SIGUSR2, handle_usr2)
      usr2 = 1

  def run(self):
    #for i in range(0,10):
    while True:
      time.sleep(self.poll_time)
      print "ola"
      #event = self.fam_conn.nextEvent()
      #print event.filename, event.code2str()

# TODO: USER OS.PATH.GETMTIME() !!!
# TODO: use os.open and os.fstat to monitor log file access times
# TODO: and os.ST_ATIME, os.ST_MTIME and os.ST_CTIME in particular
# TODO:
# TODO: use time module to get current time -- perhaps time.time() and
# TODO: convert from fstat to long format and compare

class PyLogV:
  def start_file_monitor(self):
    self.fm = File_Monitor(self, "/home/mano/teste.fam", 4)
    self.fm.start()

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

    self.start_file_monitor()

if __name__ == '__main__':
  gtk.gdk.threads_init()
  list = sys.argv[1:]
# create the window
  window = PyLogV(list)

  gtk.gdk.threads_enter()
  gtk.main()
  gtk.gdk.threads_leave()
