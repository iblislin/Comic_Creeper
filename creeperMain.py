#!/usr/bin/env python2
import pygtk
pygtk.require("2.0")
import gtk
import httplib
from bs4 import BeautifulSoup

class creeper:
	def __init__(self):
		"""
		Layout:
		+ VBox2 --------------------------------------------------+
		|  + MenuBar1 -------------------------------------------+|
		|  + HBox1 ----------------------------------------------+|
		|  | label1 | ComicID | SearchBtn | CloseBtn             ||
		|  +-----------------------------------------------------+|
		|  + NoteBook1-------------------------------------------+|
		|  |  + VBox1 ------------------------------------------+||
		|  |  |  + frame2 +                                     |||
		|  |  |  | label2 |                                     |||
		|  |  |  +--------+                                     |||
		|  |  |  + frame1 -----------+                          |||
		|  |  |  |  + table1 ------+ |                          |||
		|  |  |  |  | Button | ... | |                          |||
		|  |  |  |  +--------+-----+ |                          |||
		|  |  |  |  |  ...   | ... | |                          |||
		|  |  |  |  +--------------+ |                          |||
		|  |  |  +-------------------+                          |||
		|  |  +-------------------------------------------------+||
		|  +-----------------------------------------------------+|
		|  + FSpeparator ----------------------------------------+|
		|  + StatusBar ------------------------------------------+|
		+---------------------------------------------------------+
		"""
		self.window = gtk.Window()
		self.window.set_title("Comic Creeper")
		self.window.set_size_request(600, 400)
		self.window.connect("delete_event", self.delete)
		
		# StatusBar
		self.StatusBar = gtk.Statusbar()
		self.StatusBar.push(0, "Ready")
		self.StatusBar.show()
		
		# Label
		self.label1 = gtk.Label("Comic ID")
		self.label1.set_justify(gtk.JUSTIFY_CENTER)
		self.label1.set_line_wrap(True)
		self.label1.show()

		# Frame for showing comic index
		self.frame1 = gtk.Frame("Index")
		self.frame1.show()

		# Frame for showing comic info
		self.frame2 = gtk.Frame('Info')
		self.frame2.show()

		# Text entry
		self.ComicID = gtk.Entry(5)
		self.ComicID.connect('key_press_event', self.CommitComicID)
		self.ComicID.show()

		# Button for handling input ID
		self.SearchBtn = gtk.Button("Commit")
		self.SearchBtn.connect("clicked", self.Search, self.ComicID)
		self.SearchBtn.show()

		# Button for removing page
		self.CloseBtn = gtk.Button("Close")
		self.CloseBtn.connect('clicked', self.RemovePage)
		self.CloseBtn.show()

		# Foot Separator
		self.FSpeparator = gtk.HSeparator()
		self.FSpeparator.show()
		
		# Menu Widget
		## Menu Items
		self.InfoItem = gtk.MenuItem("About")
		self.InfoItem.connect('activate', self.ShowAboutInfo)
		self.InfoItem.show()
		self.AboutItem = gtk.MenuItem("About")
		self.AboutItem.show()
		## Menu ( Container )
		self.Menu1 = gtk.Menu()
		self.Menu1.show()
		## Menu Bar
		self.MenuBar1 = gtk.MenuBar();
		self.MenuBar1.show()
		## Packing
		self.Menu1.append(self.InfoItem)
		self.AboutItem.set_submenu(self.Menu1)
		self.MenuBar1.append(self.AboutItem)
		
		# NoteBook Widget
		self.NoteBook1 = gtk.Notebook()
		self.NoteBook1.popup_enable()
		self.NoteBook1.set_scrollable(True)
		self.NoteBook1.show()
		
		# Packing
		self.VBox1 = gtk.VBox(False, 0)
		self.VBox2 = gtk.VBox(False, 0)
		self.HBox1 = gtk.HBox(True, 5)
		self.HBox1.pack_start(self.label1, False, True, 0)
		self.HBox1.pack_start(self.ComicID, True, True, 0)
		self.HBox1.pack_start(self.SearchBtn, False, True, 0)
		self.HBox1.pack_start(self.CloseBtn, False, True, 0)
		self.HBox1.show()
		self.VBox1.pack_start(self.frame2, True, True, 0)
		self.VBox1.pack_start(self.frame1, True, True, 0)
		self.VBox1.show()
		self.NoteBook1.append_page(self.VBox1, gtk.Label('main'))
		self.VBox2.pack_start(self.MenuBar1, False, True, 0)
		self.VBox2.pack_start(self.HBox1, False, True, 0)
		self.VBox2.pack_start(self.NoteBook1, True, True, 0)
		self.VBox2.pack_start(self.FSpeparator, False, True, 0)
		self.VBox2.pack_start(self.StatusBar, False, True, 0)
		self.VBox2.show()
		self.window.add(self.VBox2)
		self.window.show()
	
	def main(self):
		gtk.main()
	
	def delete(self, widget, event):
		gtk.main_quit()
		return False

	def Search(self, widget, cid):
		"""
		cid for Comic ID.
		"""
		self.ShowIndex(cid)
	
	def ShowIndex(self, cid):
		"""
		Create a new page and put the widget into it.
		"""
		url = 'www.8comic.com'
		
		# Checking input data if a numbe
		if cid.get_text().isdigit() == False :
			self.StatusBar.push(0, "Please input a Comic ID!")
			return
		
		# Frame for showing comic index
		TmpFrame1 = gtk.Frame("Index")
		TmpFrame1.show()
		
		# Frame for showing comic info
		TmpFrame2 = gtk.Frame('Info')
		TmpFrame2.show()
		
		src = self.GetWebData(url, '/html/' + cid.get_text() + '.html')
		if src == None :
			return
		# Get the index
		index = self.GetComicIndex(src)
		# Get the images code
		imgcode = self.GetImgCode(cid)
		## Packing index buttons with table
		row = len(index) // 5
		row += 1 if ((len(index) % 5) != 0) else 0
		TmpTable = gtk.Table(1, 1, True)
		num = len(index)
		k = 0
		for i in range(0, row):
			for j in range(0, 5 if num > 5 else num):
				btn = gtk.Button(index[k])
				btn.connect('clicked', self.ShowImgPage, imgcode[k], index[k])
				k += 1
				TmpTable.attach(btn, j, j+1, i, i+1)
				btn.show()
			num -= 5
		TmpTable.show()
		TmpFrame1.add(TmpTable)
		
		# Get Comic Info
		info = self.GetComicInfo(src)
		tmps = ''
		tmps = '%s\n%s:\t%s' % (tmps, 'Name', info['Name'])
		tmps = '%s\n%s:\t%s' % (tmps, 'Intro', info['Intro'])
		TmpLabel = gtk.Label(tmps)
		TmpLabel.set_line_wrap(True)
		TmpLabel.show()
		## Get Comic Cover
		cover = gtk.Image()
		rawimg = self.GetWebData('www.8comic.com', '/pics/0/' + cid.get_text() + 's.jpg', False)
		loader = gtk.gdk.PixbufLoader()
		loader.write(rawimg)
		loader.close()
		cover.set_from_pixbuf(loader.get_pixbuf())
		cover.show()
		## Packing
		TmpHBox1 = gtk.HBox(False, 0)
		TmpHBox1.pack_start(cover, True, True, 0)
		TmpHBox1.pack_start(TmpLabel, True, True, 0)
		TmpHBox1.show()
		TmpFrame2.add(TmpHBox1)
		del tmps
		
		# Packing
		TmpVBox1 = gtk.VBox(False, 0)
		TmpVBox1.pack_start(TmpFrame2, True, True, 0)
		TmpVBox1.pack_start(TmpFrame1, True, True, 0)
		TmpVBox1.show()
		# New Page
		self.NoteBook1.append_page(TmpVBox1, gtk.Label(info['Name']));
	
	def GetWebData(self, host, path, ConvertFlag=True):
		get = httplib.HTTPConnection(host)
		
		get.request('GET', path, '', {'Referer': 'http://' + host + '/',
			'User-Agent': 'Mozilla/5.0  AppleWebKit/537.11 (KHTML, like Gecko)\
			Chromium/23.0.1271.97 Chrome/23.0.1271.97 Safari/537.11'})
		self.StatusBar.push(0, 'Loading')
		index = get.getresponse()
		self.StatusBar.push(0, str(index.status) + ' ' + index.reason)
		
		# Checking http status code
		if index.status != 200:
			get.close()
			return
		
		if ConvertFlag == True:
			data = index.read().decode('big5')
		else:
			data = index.read()
		get.close()
		return data

	def GetComicIndex(self, src):
		index = BeautifulSoup(src)
		ls = []

		# Remove needless string
		for i in index.find(id='rp_ctl00_tb_comic').find_all('script'):
			i.decompose()
		
		# Generate the index
		for i in index.find(id='rp_ctl00_tb_comic').table.find_all('table'):
			if i == index.find(id='rp_ctl00_tb_comic').table.table:
				continue	# Ignore the first table
			for j in i.stripped_strings:
				ls.append(j)
			
		return ls

	def GetComicInfo(self, src):
		src = BeautifulSoup(src)
		dic = {}
		
		# Get the comic name
		dic.update({'Name': 
			src.table.find_next_sibling('table').table.table.table.get_text('', True)})

		# Get the comic introduction
		dic.update({'Intro':
			src.table.find_next_sibling('table').table.find_all('td')[-1].get_text('', True)})
		
		return dic

	def CleanFrame(self, widget):
		self.frame1.remove(self.table1)
		self.frame2.remove(self.label2)
		self.ComicID.set_text('')
		self.StatusBar.push(0, 'Ready')
	
	def RemovePage(self, widget):
		page = self.NoteBook1.get_current_page()
		self.NoteBook1.remove_page(page)

	def GetImgCode(self, cid):
		"""
		This function will generate a tow dimension list.
		"""
		src = self.GetWebData('www.8comic.com', '/view/' + cid.get_text() + '.html')
		codes= BeautifulSoup(src)
		codes = str(codes.find_all('script', src='')[-1])
		start = codes.find('var codes=')
		end = codes.find('.split(\'|\')')
		codes = codes[start+11:end-1].split('|')
		
		# Simulating the decoding
		itemid = cid.get_text()
		ls = []
		for i in codes:
			num = i.split(' ')[0]
			sid = i.split(' ')[1]
			did = i.split(' ')[2]
			page = i.split(' ')[3]
			code = i.split(' ')[4]
			ch = int(num) # ch for Chapter
			j = []
			for p in range(1, int(page)+1):
				m = (((p - 1) // 10) % 10) + (((p - 1) % 10) * 3)
				if p < 10:
					img = "00" + str(p)
				elif p < 100:
					img = "0" + str(p)
				else:
					img = str(p)
				img += '_' + code[m:m+3]
				url = 'img' + sid + ".8comic.com"
				path = "/" + did + "/" + itemid + "/" + num + "/" + img + ".jpg"
				j.append((url, path))
			ls.append(j)
		
		return ls
	
	def ShowAboutInfo(self, widget):
		m = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		m.set_markup("Comic Creeper")
		m.action_area.get_children()[0].connect('clicked', lambda widget: m.destroy())
		m.show()
	
	def CommitComicID(self, widget, event):
		if event.keyval == 65293:
			self.Search(widget, self.ComicID)
	
	def ShowImgPage(self, widget, UrlList, TabName):
		# VBox
		TmpVBox1 = gtk.VBox(True, 0)
		TmpVBox1.show()
		
		# New Page
		self.NoteBook1.append_page(TmpVBox1, gtk.Label(TabName))
		
		# Show images
		image = gtk.Image()
		rawimg = self.GetWebData(UrlList[0][0], UrlList[0][1], False)
		loader = gtk.gdk.PixbufLoader()
		loader.write(rawimg)
		loader.close()
		image.set_from_pixbuf(loader.get_pixbuf())
		image.show()
		
		# Packing
		TmpVBox1.pack_start(image, True, True, 0)

if __name__ == '__main__':
	cc = creeper()
	cc.main()
