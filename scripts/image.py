import wx
from typing import Optional
from PIL import Image as PImage

def pimgResize(image:PImage.Image, size:Optional[tuple]=None,resample:int=PImage.ANTIALIAS) -> PImage.Image:
	if size is None:
		size = image.size
	return image.resize(size,resample)

def pimg2wxbitmap(image:PImage.Image) -> wx.Bitmap:
	width, height = image.size
	return wx.Bitmap.FromBuffer(width, height, image.tobytes())
	
def wxbitmap2pimg(image:wx.Bitmap) -> PImage.Image:
	bitmap = image
	size = tuple(bitmap.GetSize())
	data = bitmap.ConvertToImage().GetData()
	return PImage.frombuffer('RGB', size, bytes(data), 'raw', 'RGB', 0, 1)

def scale_bitmap(bitmap:wx.Bitmap, width, height) -> wx.Bitmap:
	image = bitmap.ConvertToImage()
	image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
	return wx.Bitmap(image)

class Image:
	def __init__(self) -> None:
		self.__list_undo = []
		self.__list_redo = []
		self.__current_image = None

	@property
	def current(self) -> wx.Bitmap:
		return self.__current_image
	@current.setter
	def current(self, image):
		self.insert(image)

	def undo(self):
		if self.__list_undo:
			self.__list_redo.append(self.current)
			self.current = self.__list_undo.pop()

	def redo(self):
		if self.__list_redo:
			self.__list_undo.append(self.current)
			self.current = self.__list_redo.pop()

	def insert(self, image) -> None:
		if isinstance(image, wx.Bitmap):
			self.insertWxBitmap(image)
		elif isinstance(image, PImage.Image):
			self.insertPimage(image)
		else:
			class_name = image.__class__.__name__
			raise TypeError(f'no supported type "{class_name}" for image object.')

	def insertWxBitmap(self, image:wx.Bitmap) -> None:
		if self.__current_image is not None:
			self.__list_undo.append(self.__current_image)
		self.__current_image = image

	def insertPimage(self, image:PImage.Image)-> None:
		if self.__current_image is not None:
			self.__list_undo.append(self.__current_image)
		bitmap = pimg2wxbitmap(image)
		self.insertWxBitmap(bitmap)

	def toPimage(self)-> PImage.Image:
		if self.__current_image is None:
			return None
		return wxbitmap2pimg(self.__current_image)
	