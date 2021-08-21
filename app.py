import wx
import os.path as Path
import scripts.image as Simage

class MainWindow(wx.Frame):

	def __init__ (self, parent):

		super(MainWindow, self) .__init__(parent, title='ImageEditor-v0.0.2')
		self.SetSize((600,500))
		self.SetWindowStyle(wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
		self.SetIcon(wx.Icon('images/icon.ico',type=wx.BITMAP_TYPE_ICO))

		self.menubar = wx.MenuBar()
		#self.Bind(wx.EVT_MENU, self.__OnQuit, fileItem)
		self.SetMenuBar(self.menubar)
		self.toolbar = self.CreateToolBar()
		self.toolbar.SetBackgroundColour('#002222')
		
		icon = wx.Bitmap('images/icon.ico',type=wx.BITMAP_TYPE_ICO)
		icon = Simage.scale_bitmap(icon,20,20)
		self.toolbar.AddTool(21, 'vaca', icon)
		self.Bind(wx.EVT_MENU,self.__OnQuit)
		self.toolbar.Realize()

		# print(menubar.GetHelpString(10))
		self.statusbar = self.CreateStatusBar()
		self.statusbar.SetStatusText ('')
		self.setMenuBar()

		painel = wx.Panel(self)
		hbox = wx.BoxSizer(wx.HORIZONTAL)

		self.listbox = wx.ListBox(painel)

		hbox.Add(self.listbox,1, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, 20)
		hbox.SetDimension(0,0,80,-1)

		img_panel = wx.Panel(painel)
		vbox = wx.BoxSizer(wx.VERTICAL)
		
		self.W_MAX_IMG = 300
		self.H_MAX_IMG = 400

		img = wx.Image(self.W_MAX_IMG,self.H_MAX_IMG)
		self.static_bitmap = wx.StaticBitmap(img_panel, wx.ID_ANY,size=(self.W_MAX_IMG,self.H_MAX_IMG))
		self.static_bitmap.SetBackgroundColour(wx.Colour(140, 140, 140))
		#self.currentImage.SetBitmap(wx.Bitmap('images/icon.ico',type=wx.BITMAP_TYPE_ICO))
		#self.currentImage.SetBitmap(wx.Bitmap('images/icon.ico',type=wx.BITMAP_TYPE_ICO))
		vbox.Add(self.static_bitmap,1,wx.CENTER | wx.ALL, 20)
		img_panel.SetSizer(vbox)

		hbox.Add(img_panel,1,wx.CENTER, wx.CENTER)
		painel.SetSizer(hbox)

		self.Center()
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
	
	def OnCloseWindow(self, event):
		''' 
		messagebox = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
			 wx.YES_NO | wx.CENTRE | wx.NO_DEFAULT  | wx.ICON_INFORMATION)

		response = messagebox.ShowModal()

		if response == wx.ID_YES:
			self.Destroy()
		else:
			event.Veto() '''
		self.Destroy()

	def setFileMenu(self):
		menu = wx.Menu()
		self.menubar.Append(menu, '&File')

		file_open = menu.Append(wx.ID_OPEN,'abrir arquivo\tCtrl+R')
		file_open.SetHelp(helpString ='abre uma arquivo')
		self.Bind(wx.EVT_MENU, self.OnOpen, file_open)

		file_save = menu.Append(wx.ID_SAVE,'salvar arquivo\tCtrl+S')
		file_save.SetHelp(helpString ='salva uma arquivo')
		file_save_as = menu.Append(wx.ID_SAVE,'salvar como')
		file_save_as.SetHelp(helpString ='salva uma arquivo como\tCtrl+Shift+S')
		menu.AppendSeparator()

	def setImageMenu(self):

		menu = wx.Menu()
		self.menubar.Append(menu, '&Image')

		submenu = menu.Append(wx.ID_ANY,'cortar')
		submenu.SetHelp(helpString ='cortar imagem')
		#self.Bind(wx.EVT_MENU, self.OnOpen, submenu)
		submenu = menu.Append(wx.ID_ANY,'rotacionar')
		submenu.SetHelp(helpString ='rotaciona a imagem')
		#self.Bind(wx.EVT_MENU, self.OnOpen, submenu)
		submenu = menu.Append(wx.ID_ANY,'redimensionar')
		submenu.SetHelp(helpString ='redimensiona a imagem')
		#self.Bind(wx.EVT_MENU, self.OnOpen, submenu)
		submenu = menu.Append(wx.ID_ANY,'inverter')
		submenu.SetHelp(helpString ='inverte a imagem')
		#self.Bind(wx.EVT_MENU, self.OnOpen, submenu)
		menu.AppendSeparator()

	def setFilterMenu(self):
		menu = wx.Menu()
		self.menubar.Append(menu, '&Filter')
		submenu = menu.Append(wx.ID_ANY,'rgb to gray')
		submenu.SetHelp(helpString ='converte para escala de cinza')

		submenu = menu.Append(wx.ID_ANY,'cortar')
		submenu.SetHelp(helpString ='cortar imagem')
		#self.Bind(wx.EVT_MENU, self.OnOpen, submenu)
		#self.Bind(wx.EVT_MENU, self.OnOpen, submenu)
	def setEditMenu(self):
		menu = wx.Menu()
		self.menubar.Append(menu, '&Edit')

	def onClose(self):
		self.Destroy()

	def setMenuBar(self):
		#image_menu.SetHelpString(wx.ID_ANY,helpString='opceos de imagem')
		self.setFileMenu()
		self.setEditMenu()
		self.setImageMenu()
		self.setFilterMenu()
		
	def updateImage(self, img):
		size = img.GetSize()
		w,h = size.Width, size.Height
		scale = self.W_MAX_IMG/max(w,h)
		
		imagepil = Simage.wxbitmap2pimg(img)
		w,h = int(scale*w),int(scale*h)
		imagepil = Simage.pimgResize(imagepil,(w,h))

		img = Simage.pimg2wxbitmap(imagepil)
		self.static_bitmap.SetBitmap(img)
		self.static_bitmap.SetSize(0,0,w,h)
		self.static_bitmap.Center()

	def OnOpen(self,e):
		''' Open a file'''
		files_extensions = [
			'PNG image (*.png)|*.png',
			'JPG image (*.jpg)|*.jpg',
			'Icon (*.ico)|*.ico',
			'All files (*.*)|*.*'
		]
		wildcard = '|'.join(files_extensions)
		dlg = wx.FileDialog(self, 'Choose a file', '', '',wildcard, wx.FD_OPEN)
		dlg.Center()
		if dlg.ShowModal() == wx.ID_OK:
			img = wx.Bitmap(dlg.GetPath())
			filename,_ = Path.splitext(dlg.GetFilename())
			self.listbox.InsertItems([str(self.listbox.GetCount())+' - '+filename],self.listbox.GetCount())
			self.listbox.SetSelection(self.listbox.GetCount()-1)
			self.updateImage(img)

		dlg.Destroy()

	def __OnQuit(self, event):
		self.Destroy()
		#if event.GetMenu() == self.quit_menu:


if __name__ == '__main__':

	app = wx.App()
	frame = MainWindow(None)
	frame.Show()
	app.MainLoop ()