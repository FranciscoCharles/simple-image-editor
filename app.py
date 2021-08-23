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
		
		self.SetMenuBar(self.menubar)
		self.toolbar = self.CreateToolBar()
		self.toolbar.SetBackgroundColour('#002222')
		
		icon = wx.Bitmap('images/icon_exit.ico',type=wx.BITMAP_TYPE_ICO)
		icon = Simage.scale_bitmap(icon,35,40)
		shortcut_exit = self.toolbar.AddTool(21, 'exit', icon)
		self.Bind(wx.EVT_TOOL,self.__OnQuit,shortcut_exit)
		self.toolbar.Realize()

		self.statusbar = self.CreateStatusBar()
		self.statusbar.SetStatusText ('')

		self.setMenuBar()

		painel = wx.Panel(self)
		hbox = wx.BoxSizer(wx.HORIZONTAL)

		self.listbox = wx.ListBox(painel)
		self.listbox.Bind(wx.EVT_LISTBOX,self.onChanceItemList)

		hbox.Add(self.listbox,1, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, 20)
		hbox.SetDimension(0,0,80,-1)

		img_panel = wx.Panel(painel)
		vbox = wx.BoxSizer(wx.VERTICAL)
		
		self.W_MAX_IMG = 300
		self.H_MAX_IMG = 400

		self.list_images = []
		self.current_image = None

		self.static_bitmap = wx.StaticBitmap(img_panel, wx.ID_ANY,size=(self.W_MAX_IMG,self.H_MAX_IMG))
		self.static_bitmap.SetBackgroundColour(wx.Colour(140, 140, 140))

		vbox.Add(self.static_bitmap,1,wx.CENTER | wx.ALL, 20)
		img_panel.SetSizer(vbox)

		hbox.Add(img_panel,1,wx.CENTER, wx.CENTER)
		painel.SetSizer(hbox)

		self.Center()
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

	def onChanceItemList(self, event):
		index_item = self.listbox.GetSelection()
		self.current_image = self.list_images[index_item]
		image = self.current_image.current
		self.updateImage(image)

	def onUndo(self,event):
		if self.current_image:
			self.current_image.undo()
		
	def onRedo(self,event):
		if self.current_image:
			self.current_image.redo()

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

		file_open = menu.Append(wx.ID_OPEN,'open file\tCtrl+R')
		file_open.SetHelp(helpString ='open file')
		self.Bind(wx.EVT_MENU, self.OnOpenFile, file_open)

		file_open = menu.Append(wx.ID_OPEN,'open folder\tCtrl+Shift+R')
		file_open.SetHelp(helpString ='open folder')
		menu.AppendSeparator()

		file_save = menu.Append(wx.ID_SAVE,'save\tCtrl+S')
		file_save.SetHelp(helpString ='save file')

		file_save_as = menu.Append(wx.ID_SAVE,'save as\tCtrl+Shift+S')
		file_save_as.SetHelp(helpString ='save file as')
		self.menubar.Append(menu, '&File')

	def setImageMenu(self):

		menu = wx.Menu()

		submenu = menu.Append(wx.ID_ANY,'cut')
		submenu.SetHelp(helpString ='cut image')
		#self.Bind(wx.EVT_MENU, self.OnOpenFile, submenu)
		submenu = menu.Append(wx.ID_ANY,'rotate')
		submenu.SetHelp(helpString ='rotate image')
		#self.Bind(wx.EVT_MENU, self.OnOpenFile, submenu)
		submenu = menu.Append(wx.ID_ANY,'resize')
		submenu.SetHelp(helpString ='resize imagem')
		#self.Bind(wx.EVT_MENU, self.OnOpenFile, submenu)
		submenu = menu.Append(wx.ID_ANY,'invert')
		submenu.SetHelp(helpString ='invert image')
		#self.Bind(wx.EVT_MENU, self.OnOpenFile, submenu)
		self.menubar.Append(menu, '&Image')

	def setFilterMenu(self):
		menu = wx.Menu()

		submenu = menu.Append(wx.ID_ANY,'blur')
		submenu = menu.Append(wx.ID_ANY,'gray')
		submenu.SetHelp(helpString ='convert to gray scale')
		submenu = menu.Append(wx.ID_ANY,'laplace')
		submenu = menu.Append(wx.ID_ANY,'prewitt')
		submenu = menu.Append(wx.ID_ANY,'scharr')
		submenu = menu.Append(wx.ID_ANY,'sobel')

		self.menubar.Append(menu, '&Filter')
		
	def setEditMenu(self):
		menu = wx.Menu()

		submenu = menu.Append(wx.ID_ANY,'undo\tCtrl+Z')
		submenu.SetHelp(helpString ='undo image')
		self.Bind(wx.EVT_MENU, self.onUndo, submenu)

		submenu = menu.Append(wx.ID_ANY,'undo all\tCtrl+Shift+Z')
		submenu.SetHelp(helpString ='undo all images')

		submenu = menu.Append(wx.ID_ANY,'redo\tCtrl+Y')
		self.Bind(wx.EVT_MENU, self.onRedo, submenu)
		submenu.SetHelp(helpString ='redo image')

		submenu = menu.Append(wx.ID_ANY,'redo all\tCtrl+Shift+Y')
		submenu.SetHelp(helpString ='redo all images')

		self.menubar.Append(menu, '&Edit')
	def onClose(self):
		self.Destroy()

	def setMenuBar(self):
		#image_menu.SetHelpString(wx.ID_ANY,helpString='opceos de imagem')
		self.setFileMenu()
		self.setEditMenu()
		self.setFilterMenu()
		self.setImageMenu()
		
	def updateImage(self, new_bitmap):
		size = new_bitmap.GetSize()
		w,h = size.Width, size.Height
		scale = self.W_MAX_IMG/max(w,h)
		
		imagepil = Simage.wxbitmap2pimg(new_bitmap)
		w,h = int(scale*w),int(scale*h)
		imagepil = Simage.pimgResize(imagepil,(w,h))

		bitmap = Simage.pimg2wxbitmap(imagepil)
		self.static_bitmap.SetBitmap(bitmap)
		self.static_bitmap.SetSize(0,0,w,h)
		self.static_bitmap.Center()

	def OnOpenFile(self,e):
		''' Open a file'''
		files_extensions = [
			'PNG image (*.png)|*.png;',
			'JPG image (*.jpg)|*.jpg;',
			'Icon (*.ico)|*.ico;',
			'Any image (*.png,*.jpg,*.ico)|*.png;*.jpg;*.ico'
		]
		wildcard = '|'.join(files_extensions)
		dialog = wx.FileDialog(self, 'Choose a file', '', '',wildcard, wx.FD_OPEN)
		dialog.Center()
		
		if dialog.ShowModal() == wx.ID_OK:
			image = Simage.Image()
			image.current = wx.Bitmap(dialog.GetPath())
			filename,_ = Path.splitext(dialog.GetFilename())
			label = f'{self.listbox.GetCount()} - {filename}'
			self.listbox.InsertItems([label],self.listbox.GetCount())
			self.listbox.SetSelection(self.listbox.GetCount()-1)
			self.updateImage(image.current)
			self.list_images.append(image)

		dialog.Destroy()

	def __OnQuit(self, event):
		self.Destroy()
		#if event.GetMenu() == self.quit_menu:


if __name__ == '__main__':

	app = wx.App()
	frame = MainWindow(None)
	frame.Show()
	app.MainLoop ()