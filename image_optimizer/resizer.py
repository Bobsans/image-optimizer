import math

from PIL import Image


class ResizePattern:
    __slots__ = ('limiter', 'width', 'height', 'force')

    def __init__(self, limiter: str, width: int, height: int, force: bool = False):
        self.limiter = limiter
        self.width = width
        self.height = height
        self.force = force

    @property
    def size(self):
        return self.width, self.height

    @property
    def limitfn(self):
        return {'min': max, 'max': min}.get(self.limiter)

    def calculate_size(self, image):
        iw, ih = image.size
        if self.limitfn:
            ratio = self.limitfn(self.width / iw, self.height / ih)
            return math.ceil(iw * ratio), math.ceil(ih * ratio)
        return self.size

    def has_need_resize(self, image):
        w, h = image.size
        return (self.limiter == 'min' and (w < self.width or h < self.height)) or (self.limiter == 'max' and (w > self.width or h > self.height)) or self.limitfn is None or self.force

    def __str__(self):
        return ''.join((
            'w=%s h=%s' % (self.width, self.height),
            (' l=%s' % self.limiter) if self.limitfn else '',
            ' f' if self.force else ''
        ))

    def __repr__(self):
        return '<ResizePattern(' + self.__str__() + ')>'


class Resizer:
    @staticmethod
    def resize(image: Image, pattern: ResizePattern):
        if pattern.has_need_resize(image):
            return image.resize(pattern.calculate_size(image), Image.ANTIALIAS)
        return image

    @classmethod
    def crop(cls, image: Image, pattern: ResizePattern, anchor: str = 'center'):
        image = cls.resize(image, pattern)
        w, h = image.size

        if w > pattern.width:
            if anchor == 'top':
                image = image.crop((0, 0, pattern.width, pattern.height))
            elif anchor == 'center':
                image = image.crop(((w - pattern.width) / 2, 0, (w + pattern.width) / 2, pattern.height))
            elif anchor == 'bottom':
                image = image.crop((w - pattern.width, 0, pattern.width, pattern.height))
            else:
                raise ValueError('Invalid value for crop_type')
        elif h > pattern.height:
            if anchor == 'top':
                image = image.crop((0, 0, pattern.width, pattern.height))
            elif anchor == 'center':
                image = image.crop((0, (h - pattern.height) / 2, pattern.width, (h + pattern.height) / 2))
            elif anchor == 'bottom':
                image = image.crop((0, h - pattern.height, pattern.width, pattern.height))
            else:
                raise ValueError('Invalid value for crop_type')

        return image
