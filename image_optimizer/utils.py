import logging
import sys
from collections import OrderedDict

SIZES = OrderedDict((('kb', 1024), ('mb', 1024 ** 2), ('gb', 1024 ** 3)))


def format_size_parts(value, force=None):
    multipler = -1 if value < 0 else 1
    value = abs(value)

    if isinstance(force, str):
        force = force.lower()
        if force == 'b':
            return value * multipler, 'b'
        else:
            if force in SIZES:
                return (value / SIZES[force]) * multipler, force.capitalize()
            else:
                raise ValueError('Ivalid force value.')

    if value < 1024:
        return value * multipler, 'b'

    for ext, val in SIZES.items():
        if value < val * 1024:
            return (value / val) * multipler, ext.capitalize()


def format_size(value, force=None):
    value, ext = format_size_parts(value, force)

    if ext == 'b':
        return '%i b' % value
    else:
        return '%.2f %s' % (value, ext)


def decode(path):
    return path.encode(sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding)


def make_logger():
    logger = logging.getLogger('image_optimizer')
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
