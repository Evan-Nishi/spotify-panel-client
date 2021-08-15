from PIL import Image

class ImageHelper:
    def pixelate(self, file_name):
        img = Image.open('/dev/shm/{}'.format(file_name))
        res = img.resize((32,32), resample=Image.BILINEAR)
        return res