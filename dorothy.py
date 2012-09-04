from dorothy_gui import dorothyGUI
import gtk
import os, sys
from pprint import pprint as pp


class dorothy:
	
	def __init__(self):
		self.gui = dorothyGUI(self)

		self.methods = {
			'find'		: self.find,
			'define'	: self.define,
			'wiki'		: self.wiki,
			'app'		: self.app,
			'google'	: self.google,
			'amazon'	: self.amazon,
			'calc'		: self.calc
		}
		
		# These are our available key binds.
		self.bindings = {
			0 : [],	# Press 0 to select this result option (later it becomes 'enter' key)
			1 : [],	# Press 1 to select this result option	
			2 : [],	# Press 2 to select this result option	
			3 : [],	# Press 3 to select this result option	
			4 : [],	# Press 4 to select this result option	
			5 : [],	# Press 5 to select this result option	
			6 : [],	# Press 6 to select this result option	
			7 : [],	# Press 7 to select this result option	
			8 : []	# Press 8 to select this result option	
		}
		
		# Get a list of programs installed
		self.programs = self._get_apps_info()

		# Limit our results to 5 things only
		self.result_limit = 5
	
	
	def parse_input(self, input):
		# The flow here goes like this: First see if input is a math expression.
		# If it isn't, we split input at the spaces. Now we check to see ifthe first word is
		# a method(split[0]). If it is, we bind a key to that result. If not, we do other checks.
		# read flow.txt for more info.
		self.clear_binds()
		
		# Is this a math expr? if the first char isn't alphanumeric, chances are it is.
		# could be a negarive sign, a perenthesis, etc
		try:
			r = eval(input)
			icon = self.create_icon('calc')
			self.bind_result_to_key('calc',icon, "calc", r)
		except:
			print "not evaled"
			split = input.split()
			if len(split) > 1:
				if split[0] in self.methods.keys():
					# Makes it like {1: [icon, 'define', 'niagara falls'],
					icon = self.create_icon(split[0])
					self.bind_result_to_key(split[0], icon, split[0], " ".join(split[1:]))
			else:
				 # no user-typed keywords. list matching results in apps list
				 programs = self.search_programs(input)
				 for p in programs:
					exe = self.programs[p][2]
					name = self.programs[p][0]
					icon_str = self.programs[p][1]
				 	icon = self.create_icon('app', icon_str, exe)
				 	self.bind_result_to_key(name, icon, "app", exe)
				 	
				 self.bind_result_to_key('amazon', self.create_icon('amazon'), "amazon", input)
				 self.bind_result_to_key('google', self.create_icon('google'), "google", input)
				 self.bind_result_to_key('wiki', self.create_icon('wiki'), "wiki", input)
		self.gui.add_result()
			
				
	def create_icon(self, cat, icon_str = None, exe = None):
		# Creates icons to be shown in results
		if cat == 'calc':
			it = gtk.IconTheme()
			p = os.path.dirname(os.path.abspath(__file__)) + "/icons/calculator.png"
			pb = gtk.gdk.pixbuf_new_from_file(p)
		elif cat == 'app':
			# Some apps need adjusting. for instance, pycrust's .desktop file has this:
			# Icon=/usr/share/pixmaps/pycrust. This here will not work. we have to split at /
			# and take the last bit (pycrust). But not all will work this way. Python's is
			# Icon=/usr/share/pixmaps/python2.6.xpm. Passing python2.6.xpm to load_icon()
			# will give an error. 			
			try:
				# icon_str has an icon in system's icon theme
				it = gtk.IconTheme()
				a = icon_str.split('/')[-1]
				pb = it.load_icon(a, 32, gtk.ICON_LOOKUP_FORCE_SVG)
			except:
				try:
					# icon_str is a path to an image somewhere
					pb = gtk.gdk.pixbuf_new_from_file(icon_str)
				except:
					try:
						# Sometimes there is an image im /usr/share/pixmaps with the proram's name
						pb = it.load_icon(exe, 32, gtk.ICON_LOOKUP_FORCE_SVG)
					except:
						# And when there isn't use a generic terminal icon
						p = os.path.dirname(os.path.abspath(__file__)) + "/icons/terminal.png"
						pb = gtk.gdk.pixbuf_new_from_file(p)
		else:
			#print "Cat: %s" % cat
			uri = os.path.dirname(os.path.abspath(__file__)) + "/icons/%s.png" % cat
			#uri = './icons/%s.png' % cat
			pb = gtk.gdk.pixbuf_new_from_file(uri)
			
		img = gtk.Image()
		img.set_from_pixbuf(pb)
		return img
				
	def clear_binds(self):
		for key in self.bindings:
			self.bindings[key] = []
			
			
	def bind_result_to_key(self, name, icon, keyword, input):
		# Fills up our self.bindings. So each key has a list as value, a list is in the format
		# of [name, icon, keyword , input]. The only reason we pass a 'name' is so that we can
		# look it up in the self.programs dictionary, since the keys are name.
		for key in self.bindings:
			if not self.bindings[key]:
				self.bindings[key].append(name)
				self.bindings[key].append(icon)
				self.bindings[key].append(keyword)
				self.bindings[key].append(input)
				break

	
	def launch(self, key, gui):
		# Does whatever shortcut key user pressed
		#print self.bindings[key]
		name, icon, keyword, arg = self.bindings[key]
		self.methods[keyword](arg)
		gui.delete_last_char = True
		# hide the gui
		gtk.main_quit()
		sys.exit(1)
		self.window.destroy()
		
	def define(self, term):
		import webbrowser
		url = "http://dictionary.reference.com/browse/%s" % term
		webbrowser.open(url)
		
	def find(self, term):
		print "find called"
	
	def wiki(self, query):
		print "wiki called"
		
	def app(self, name):
		''' launches an app'''
		import subprocess
		subprocess.Popen(name)
		
	def amazon(self, query):
		import webbrowser
		query = query.replace(" ", "+")
		url = "http://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords="
		url += query + "&x=0&y=0"
		webbrowser.open(url)

	def google(self, query):
		import webbrowser
		query = query.replace(" ", "+")
		url = "https://www.google.com/search?ie=UTF-8&q=" + query
		webbrowser.open(url)
	
	def calc(self, result):
		#TODO copy result to clipboard?
		pass
				
	def search_programs(self, word):
		# Return a list of programs that match what the user typed
		# We only return a list of self.result_limit number of elements.
		return [p for p in self.programs.keys() if p.find(word) == 0][0:self.result_limit]

		
		
	def _get_apps_info(self):
		# Creates a dictionay with the format { name : [name, icon string, executable] }	
		path = "/usr/share/applications/"
		apps =  os.listdir(path)
		apps.sort()
		ret = {}
		for app in apps:

			if not os.path.isdir(path+app):
				# info is something like [name, icon_str, executable], so we store it
				# like {name.lower() : [name, icon, executable]}, so when user starts typing
				# we try to match what he's typed with 'name' in the dict key. 
				info = self.parse_desktop_file(path+app)
				if not info == None:
					ret[info[0]] = info
				
		return ret
		
		
	def parse_desktop_file(self, app):
		f = open(app)
		e = False
		i = False
		n = False
		for line in f.readlines():
			if line[0:5] == "Exec=":
				e = True
				exec_line = line.split("=")[1].strip("\r\n")
			if line[0:5] == "Icon=":
				i = True
				li = line.strip("\r\n")
				icon = line.split("=")[1].strip("\r\n")
			if line[0:5] == 'Name=':
				n = True
				name = line.split("=")[1].strip("\r\n")
				
			if e and i and n:
				exe = self.parse_line(exec_line)
				'''
				print app
				print "-" * len(app)
				print "exec: %s"%le
				print "icon: %s" %li
				print 
				'''
				#print "--------"
				#print [name, icon, exe]
				return  [name.lower(), icon, exe]
		
		
	def parse_line(self, line):
		# Line can be something like /usr/bin/python2.5 --something %U
		# or just 'pidgin', so we check. If it's the former case, we only want to end up with
		# 'python2.5 --something'
		# returns something like ['LibreOffice Base', 'libreoffice34-base', 'libreoffice --base']
		le = line.split(" ")
		if len(le) > 1:
			del le[-1]
		
		exe = ' '.join(le) 
		return exe
		
	
dorothy = dorothy()


if __name__ == "__main__":
	gtk.main()


