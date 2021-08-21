import wx
import PIL
from PIL import Image as PImage

def pimgResize(image, size=None, resample=PIL.Image.ANTIALIAS):
	if size is None:
		size = image.size
	return image.resize(size,resample)

def pimg2wxbitmap(image):
	'''
	data = image.tobytes('raw','RGBA')
	(w,h) = image.size
	return wx.Image.FromBufferRGBA(w,h,data)
	'''
	width, height = image.size
	return wx.Bitmap.FromBuffer(width, height, image.tobytes())
	
def wxbitmap2pimg(image):
	'''
	image = image.ConvertToImage()
	image = image.CopyFromBuffer(image.GetDataBuffer(), wx.BitmapBufferFormat_RGBA)
	buffer = bytes(image.GetData())
	print(type(buffer))
	size = image.GetSize()
	w,h = size.Width, size.Height
	image = PImage.frombytes('RGBA',(w,h),buffer)
	r,g,b,a = image.split()
	return PImage.merge('RGBA',(b,g,r,a))
	'''
	bitmap = image
	size = tuple(bitmap.GetSize())
	data = bitmap.ConvertToImage().GetData()
	return PImage.frombuffer('RGB', size, bytes(data), 'raw', 'RGB', 0, 1)

def scale_bitmap(bitmap, width, height):
	image = bitmap.ConvertToImage()
	image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
	result = wx.Bitmap(image)
	return result