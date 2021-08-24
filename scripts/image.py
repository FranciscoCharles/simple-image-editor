import wx
import numpy as np
from PIL import Image as PImage
from skimage.io import imsave
from typing import Optional

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
		self.__was_saved = True

	@property
	def was_saved(self):
		return self.__was_saved
	@was_saved.setter
	def was_saved(self, state:bool):
		self.__was_saved = state
	@property
	def current(self) -> np.ndarray:
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
		if isinstance(image, np.ndarray):
			self.insertNumpyArray(image)
		elif isinstance(image, wx.Bitmap):
			self.insertWxBitmap(image)
		elif isinstance(image, PImage.Image):
			self.insertPimage(image)
		else:
			class_name = image.__class__.__name__
			raise TypeError(f'no supported type "{class_name}" for image object.')
		self.was_saved = False
	def insertNumpyArray(self, image:np.ndarray) -> None:
		if self.current is not None:
			self.__list_undo.append(self.current)
		self.__current_image = image

	def insertWxBitmap(self, bitmap:wx.Bitmap) -> None:
		if self.current is not None:
			self.__list_undo.append(self.current)
		image = wxbitmap2pimg(bitmap)
		self.__current_image = np.array(image)

	def insertPimage(self, image:PImage.Image)-> None:
		if self.current is not None:
			self.__list_undo.append(self.current)
		self.__current_image = np.array(image)

	def toWxbitmap(self)->wx.Bitmap:
		if self.current is None:
			return None
		pilimage = PImage.fromarray(self.current)
		return pimg2wxbitmap(pilimage)

	def toPimage(self) -> PImage.Image:
		if self.__current_image is None:
			return None
		return PImage.fromarray(self.current)

	def normalize(self, max_value=255, array_type=np.uint8) -> np.ndarray:
		img = self.current
		diff = (img - img.min()).astype('float32')
		divider = diff.max()
		if divider == 0:
			divider = 1
		normalized_img = diff / divider
		return (max_value * normalized_img).astype(array_type)

	def save(self, filename, normalize = True, max_value = 255, array_type = np.uint8) -> None:
		
		if not isinstance(filename, str):
			raise ValueError('"filename" type must be str.')
		if normalize:
			imsave(filename, self.normalize(max_value, array_type))
		else:
			imsave(filename, self.current)
		
		self.__was_saved = True
	