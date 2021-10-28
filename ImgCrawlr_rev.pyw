#-*- coding: cp949 -*-

import wx
import urllib
import urllib2
import os


class MyDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.DIALOG_NO_PARENT
        wx.Dialog.__init__(self, *args, **kwds)
        self.text_ctrl_1 = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER)
        self.btn_start = wx.Button(self, -1, "검색!")
        self.btn_img = wx.RadioButton(self, -1, "ImageClick", style=wx.RB_GROUP)
        self.btn_google = wx.RadioButton(self, -1, "Google")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT_ENTER, self.On_Enter, self.text_ctrl_1)
        self.Bind(wx.EVT_BUTTON, self.On_Start, self.btn_start)

    def __set_properties(self):
        self.SetTitle("ImgCrawler By.Rust")
        self.SetSize((222, 83))
        self.text_ctrl_1.SetMinSize((140, 22))

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.text_ctrl_1, 0, wx.ALL, 0)
        sizer_2.Add(self.btn_start, 0, 0, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 1)
        sizer_3.Add(self.btn_img, 0, wx.EXPAND, 0)
        sizer_3.Add(self.btn_google, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        self.Centre()

    def On_Enter(self, event):
		key = self.text_ctrl_1.GetValue()
		if self.btn_img.GetValue():
			ImgProcess_imgc(key)
		else:
			ImgProcess_google(key)

    def On_Start(self, event):
		key = self.text_ctrl_1.GetValue()
		if self.btn_img.GetValue():
			ImgProcess_imgc(key)
		else:
			ImgProcess_google(key)
	
def ImgProcess_imgc(keyWord):
	nextflag = True
	input_keyword = keyWord
	search_keyword = input_keyword.replace(' ', '+')
	dirname = input_keyword + ' - ImageClick'
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

def ImgProcess_google(keyWord):
	input_keyword = keyWord
	search_keyword = input_keyword.replace(' ','+')
	dirname = input_keyword + ' - Google'
	endflag = False
	pagePos = 0
	fCnt = 0
	search_keyword = urllib.quote(search_keyword.encode('utf8'), '+')

	search_url = 'http://www.google.com/search?q='+search_keyword+'&hl=ko&tbm=isch&safe=off'

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

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    dialog_1 = MyDialog(None, -1, "")
    app.SetTopWindow(dialog_1)
    dialog_1.Show()
    app.MainLoop()
