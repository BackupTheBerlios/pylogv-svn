#! /usr/bin/env python
# -*- coding: UTF-8 -*

import pygtk
pygtk.require('2.0')

import gobject
import gtk
if gtk.pygtk_version < (2,3,90):
  print "PyGtk 2.3.90 or later required for this example"
  raise SystemExit

import gtk.glade
import re
import codecs
import sys

class PyLogV:
  def add_text(self, text):
    #iter = self.text_buffer.get_start_iter()
    #self.text_buffer.insert(iter, text)
    #u = unicode(text, "utf-8")
    #text2 = u.encode("utf-8")
    self.text_buffer.insert_at_cursor(text)
    
  def open_file(self, filename):
    #f = open(filename, 'r')
    f = codecs.open(filename, "r", "ascii")
    return f
  
  def get_text_from_file(self, f):
    return f.read()

  def delete_event(self, widget, event, data=None):
    # If you return FALSE in the "delete_event" signal handler,
    # GTK will emit the "destroy" signal. Returning TRUE means
    # you don't want the window to be destroyed.
    # This is useful for popping up 'are you sure you want to quit?'
    # type dialogs.
    #print "delete event occurred"
    
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

    print self.filename

  def add_log_file_to_log_files(self, event, data=None):
    log_file = entry.get_text()

    
    
  #def populate_log_files_text_view(self, event, data=None):
    #print self.log_file_list
    #for value in self.log_file_list:
    #  #print value
    #  text = value + '\n'
    #  self.log_files_text_buffer.insert_at_cursor(text)

    
  def __init__(self, log_file_list):
    # parse the glade file
    self.all_widgets = gtk.glade.XML("pylogv.glade")
    
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

    #self.filechooser.hide()
    self.add_button = self.all_widgets.get_widget("add")
    self.remove_button = self.all_widgets.get_widget("remove")
    self.browse_button = self.all_widgets.get_widget("browse")
    self.browse_button.connect("clicked", self.show_filechooser)
    # end window stuff

    self.preferences = self.all_widgets.get_widget("preferences")
    self.preferences.hide()
    
    self.text_view = self.all_widgets.get_widget("textview")
    self.text_buffer = self.text_view.get_buffer()

    self.entry = self.all_widgets.get_widget("entry")
    
    self.log_files = self.all_widgets.get_widget("log_files")

    model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING)
    model.append([1, "um"])
    model.append([2, "dois"])
    #iter = model.insert_before(None, None)
    #iter = None
    #self.log_files_model.append(iter)
    #iter = self.log_files_model.insert_before(None, None)
    #self.log_files_model.set_value(iter, 0, "ola")
    
    #self.log_files.set_model(self.log_files_model)
    
    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn("log_files", renderer, text=1)
    self.log_files.append_column(column)

    self.location = "undefined"
    self.color = gtk.gdk.Color(0, 0, 0)
    
    
    f = self.open_file("/var/log/errors")
    self.text = self.get_text_from_file(f)
    #print self.text
    self.add_text(self.text)


if __name__ == '__main__':
  list = []
  list = sys.argv[1:]
# create the window
  window = PyLogV(list)

  gtk.main()
