#-*- coding: cp949 -*-
import wx
import urllib2
import urllib
import os

class MyFrame(wx.Frame):
	def __init__ (self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(220, 105))
		panel = wx.Panel(self, -1)
		choice = ['ImageClick', 'Google']

		btn = wx.Button(panel, 1, "Start", (158 , 2))
		global rbox
		rbox = wx.RadioBox(panel, 2, '', (0,0), (0,0), choice , 2)
		global edtr
		edtr = wx.TextCtrl(panel, 3, '', (2,3))
		sizer = wx.GridBagSizer(1,3)
		sizer.Add(edtr,(0,0),(1,2), wx.ALL, 3)
		sizer.Add(btn,(0,3),wx.DefaultSpan, wx.ALL, 1)
		sizer.Add(rbox,(1,0),wx.DefaultSpan, wx.EXPAND)
		sizer.AddGrowableRow(1)
		sizer.AddGrowableCol(4)
		panel.SetSizerAndFit(sizer)
		self.Center()

		self.Bind(wx.EVT_BUTTON, self.OnStart, id=1)

	def OnStart(self, event):
		key = edtr.GetValue()
		if 'Google' == rbox.GetStringSelection():
			self.ImgProcess_google(key)
		else:
			self.ImgProcess_imgc(key)

	def ImgProcess_imgc(self, keyWord):
		nextflag = True
		input_keyword = keyWord
		search_keyword = input_keyword.replace(' ', '+')
		dirname = input_keyword + ' - ' + rbox.GetStringSelection()
		fCnt = 1
		pageCnt = 0
		search_keyword = urllib.quote(search_keyword.encode('utf8'), '+')
		search_url = 'http://www.imageclick.com/commercial/search.php?search='+search_keyword

		while nextflag:
			if pageCnt !=1:
				search_url += '&page='+str(pageCnt)
			req = urllib2.Request(search_url)
			opener = urllib2.build_opener()
			html = opener.open(req).read()
			before_lnk = ''
			while html.find(':view_detail') != -1:
				lnk_pos = html.find(':view_detail') + 14
				lnkend_pos = html[lnk_pos:].find('\'') + lnk_pos
				lnk = html[lnk_pos:lnkend_pos]
				if lnk == before_lnk:
					before_lnk = lnk
				else:
					before_lnk = lnk
					url = 'http://www.imageclick.com/common/view_detail.php?ProductNo='+lnk
					req = urllib2.Request(url)
					opener = urllib2.build_opener()
					new_wnd = opener.open(req).read()
					img_pos = new_wnd.find('realpreview" src=') + 18
					imgend_pos = new_wnd[img_pos:].find('\"') + img_pos
					imgurl = new_wnd[img_pos:imgend_pos]
					rfile = urllib2.urlopen(imgurl)

					imgname = imgurl.split('/')
					imgname = imgname.pop()

					if not os.path.isdir(dirname):
						os.mkdir(dirname)

					lfile = open(dirname+'\\'+imgname,'wb')
					lfile.write(rfile.read())
					rfile.close()
					lfile.close()
					lfile = open(dirname+'\\'+imgname,'rb')
					fCnt+=1
					print str(fCnt)+'. '+imgname+' is Saved'
					
				html = html[lnkend_pos:]
			pageCnt+=1
			if not '"../imgs/btn-next150.gif"' in html:
				nextflag = False

		print 'All Process Done!'

	def ImgProcess_google(self, keyWord):
		input_keyword = keyWord
		search_keyword = input_keyword.replace(' ','+')
		dirname = input_keyword + ' - ' + rbox.GetStringSelection()
		endflag = False
		pagePos = 0
		fCnt = 0
		search_keyword = urllib.quote(search_keyword.encode('utf8'), '+')

		search_url = 'http://www.google.com/search?q='+search_keyword+'&hl=ko&tbm=isch'

		while not endflag:
			if pagePos != 0:
				search_url = search_url+'&start='+str(pagePos)
			req = urllib2.Request(search_url)
			req.add_header('User-Agent', 'User-Agent:Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)')
			opener = urllib2.build_opener()
			html = opener.open(req).read()

			while html.find('imgurl=') != -1:
				img_start = html.find('imgurl=')+7
				img_end = html[img_start:].find('&amp;')+img_start
				imgurl = html[img_start:img_end]
				try:
					rfile = urllib2.urlopen(imgurl)
				except:
					html = html[img_end:]
					continue
				imgname = imgurl.split('/')
				imgname = imgname.pop()

				if imgname.rfind('.jpg') != -1:
					if len(imgname[imgname.rfind('.jpg'):]) != 4:
						imgname=imgname[:imgname.rfind('.jpg')]+'.jpg'
				elif imgname.rfind('.png') != -1:
					if len(imgname[imgname.rfind('.png'):]) != 4:
						imgname=imgname[:imgname.rfind('.png')]+'.png'
				elif imgname.rfind('.gif') != -1:
					if len(imgname[imgname.rfind('.gif'):]) != 4:
						imgname=imgname[:imgname.rfind('.gif')]+'.gif'
				else:
					head = rfile.read(2).encode('hex')
					if head == 'ffd8':
						imgname = imgname+'.jpg'
					elif head == '8950':
						imgname = imgname+'.png'
					elif head == '4749':
						imgname = imgname+'.gif'
					else:
						continue
					rfile.close()
					rfile = urllib2.urlopen(imgurl)

				if not os.path.isdir(dirname):
					os.mkdir(dirname)
				lfile = open(dirname+'\\'+imgname,'wb')
				lfile.write(rfile.read())
				rfile.close()
				lfile.close()
				lfile = open(dirname+'\\'+imgname,'rb')
				fCnt+=1
				print str(fCnt)+'. '+imgname+' is Saved'
				html = html[img_end:]

			nextlink_pos = html.rfind('<a href="/search?')
			nextlink_start = html[nextlink_pos:].find('&amp;start')+nextlink_pos
			nextlink_end = html[nextlink_start+1:].find('&amp;')+nextlink_start+1
			nextlink = html[nextlink_start:nextlink_end]
			nextlink = nextlink.replace('&amp;', '&')
			nextPos = nextlink[7:]
			if int(pagePos) < int(nextPos):
				pagePos = nextPos
			else:
				endflag = True

		print 'All Process Done!'

class MyApp(wx.App):
	def OnInit(self):
		frame = MyFrame(None, -1, 'ImgCrawlr by.Rust')
		frame.Show(True)
		return True

app = wx.App()
mainapp = MyApp(app)
mainapp.MainLoop()