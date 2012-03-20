#!/usr/bin/env python
from __future__ import division
import gobject
import pango
import pygtk
pygtk.require('2.0')
import gtk
from gtk import gdk
import cairo
import string
import pango


class dorothyGUI:
   
	def __init__(self, dorothy = None):
		self.dorothy = dorothy
		self.window = gtk.Window()
		self.window.set_border_width(10)
		self.window.set_position(gtk.WIN_POS_CENTER)
		
		
		# Used to decide wether we delete last char in gtk.entry
		self.delete_last_char = False
		
		# Create our widgets
		self.input = gtk.Entry()
		icon = gtk.Button(" R ")
		
		font = pango.FontDescription("Monospace 23")
		self.input.modify_font(font)
		
		# Widget properties
		self.input.set_has_frame(False)
		self.input.set_width_chars(30)
		
		
		# Create containers	
		self.main_box = gtk.VBox(False, 0)	# holds entire thing
		top_box = gtk.HBox(False, 10)	# holds text input & icon
		self.result_box = gtk.VBox(False, 0)	# holds result boxes
		
		# Pack widgets inside their containers
		top_box.pack_start(self.input, 0, 0, 0)
		top_box.pack_start(icon, 0, 0, 0)
		self.main_box.pack_start(top_box, 0, 0, 0)	
		self.main_box.pack_start(self.result_box, 0, 0, 0)
		
		#top_box.set_border_width(10)
		self.main_box.set_border_width(10)
		
		self.window.add(self.main_box)
		
		
		
		
		
		
		
		# Tell GTK+ that we want to draw the windows background ourself.
		# If we don't do this then GTK+ will clear the window to the
		# opaque theme default color, which isn't what we want.
		self.window.set_app_paintable(True)

		# Event handlers
		self.window.connect('expose-event', self.expose)
		self.window.connect('screen-changed', self.screen_changed)
		self.window.connect("destroy", lambda w: gtk.main_quit())
		self.window.connect("key-press-event", self.key_pressed)
		self.input.connect("changed", self.input_changed)
		
		# make it happen
		self.screen_changed(self.window)
		self.window.set_decorated(False)
		self.window.show_all()
		
		# This is kinda nasty but we need it. When there are no results to be shown,
		# we clear everything inside self.result_box, but the box doesn't resize back.
		# So, whenever there are no results to be displayed(ie, user deleted what he typed),
		# we resize the window to whatever size it is when it starts
		self.window_size = self.window.get_size()
					

	def screen_changed(self, widget, old_screen = None):
		print "screen changed"
		screen = widget.get_screen()
		colormap = screen.get_rgba_colormap()
		widget.set_colormap(colormap)


	# This is called when we need to draw the windows contents
	def expose(self, widget, e):
		cr = widget.window.cairo_create()
		
		# Draw the background
		cr.set_operator(cairo.OPERATOR_SOURCE)
		
		# Create black rectangle with 60% opacity (serves as border)
		(width, height) = widget.get_size()
		cr.set_source_rgba(0, 0, 0, 0.6)
		cr.rectangle(0, 0, width, height)
		cr.fill()
		
		# Inside the black rectangle, put a lighter one (will hold widgets)
		(width, height) = widget.get_size()
		cr.set_source_rgb(205/255, 205/255, 193/255)
		cr.rectangle(10, 10, width-20, height-20)
		cr.fill()

		return False
		

		
	
	def input_changed(self, e):
		# Called each time value of input text is changed.
		# Before showing new results, we clear old ones
		input = self.input.get_text()
		widgets = self.result_box.get_children()
		for w in widgets:
			w.destroy()
		if self.delete_last_char == True:
			self.input.set_text(input[:-1])
		if input != '':
			self.dorothy.parse_input(input)
		self.delete_last_char = False
		
		# When we remove the results, the window doesn't want to resize itself.
		# So we set the window size to whatever it was when the program started
		self.window.resize(self.window_size[0], self.window_size[1])

		
	def key_pressed(self, w, e):
		# If user pressed Q, quit.
		key = gtk.gdk.keyval_name(e.keyval).lower()
		if key == 'escape':
			gtk.main_quit()
		if key ==  'return':
				key = 0
		if e.state & gtk.gdk.SUPER_MASK:			
			key = int(key)
		if key == 'return' or key in self.dorothy.bindings.keys():
			self.dorothy.launch(key, self)
		
		# http://stackoverflow.com/questions/9651751/repainting-cairo-windows/9746742#9746742
		self.window.queue_draw()
		

		
	def add_result(self):

		# This method visually adds a 'row' with a label, and shortcut key
		for key in self.dorothy.bindings:
			value = self.dorothy.bindings[key]
			print value
			if value:
				#print "VALUE %s" % value
				icon = value[1]
				if value[2] == 'define':
					label = gtk.Label('Define %s' % value[3])
				elif value[2] == 'google':
					label = gtk.Label('Search Google for %s' % value[3])
				elif value[2] == 'wiki':
					label = gtk.Label('Search Wikipedia for %s' % value[3])
				elif value[2] == 'amazon':
					label = gtk.Label('Search Amazon for %s' % value[3])
				elif value[2] == 'ebay':
					label = gtk.Label('Search eBay for %s' % value[3])
				elif value[2] == 'calc':
					label = gtk.Label('%s' % value[3])
				elif value[2] == 'app':
					label = gtk.Label('%s' % value[0])
				else:
					label = gtk.Label()
				if key == 0:
					label_sc = gtk.Label("Enter")	
				else:
					label_sc = gtk.Label("W + %s" % key)
					
				
				fixed = gtk.Fixed()
				fixed.put(icon, 0, 0)
				fixed.put(label, 50, 0)
				fixed.put(label_sc, 450, 0)
				
				font = pango.FontDescription("Monospace 16")
				label_sc.modify_font(font)
				label.modify_font(font)

				fixed.show_all()
				self.result_box.pack_start(fixed, 0, 0, 10)
				sep = gtk.HSeparator()
				sep.show()
				self.result_box.pack_start(sep)
				
				
		
 

