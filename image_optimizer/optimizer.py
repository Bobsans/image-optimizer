import os
import re
import threading
import time
from datetime import datetime

from PIL import Image

from image_optimizer.errors import ImageOptimizerError
from image_optimizer.resizer import ResizePattern, Resizer
from image_optimizer.utils import decode, format_size, make_logger

logger = make_logger()


class Error:
    def __init__(self, file, error):
        self.file = file
        self.type = error.__class__.__name__ if isinstance(error, Exception) else 'OptimizeError'
        self.message = str(error)

    def __str__(self):
        return '%s [%s: %s]' % (self.file, self.type, self.message)


class Statistics:
    def __init__(self, optimizer):
        self.optimizer = optimizer
        self.success = []
        self.errors = []
        self.total_size_before = 0
        self.total_size_after = 0
        self.elapsed_time = 0
        self.resized = 0

    def __str__(self):
        result = [
            '\nOptimization done!\n',
            '- Elapsed time:         %s' % datetime.utcfromtimestamp(self.elapsed_time).strftime('%H:%M:%S.%f'),
        ]

        if self.optimizer.threads:
            result.append('- Threads:              %s' % self.optimizer.threads)

        result.append('- Images optimized:     %s' % len(self.success))

        if self.optimizer.resize_pattern:
            result.append('- Images resized:       %s' % self.resized)
            result.append('- Resize pattern:       %s' % self.optimizer.resize_pattern)

        result.append('- Size before:          %s (%i b)' % (format_size(self.total_size_before), self.total_size_before))
        result.append('- Size after:           %s (%i b)' % (format_size(self.total_size_after), self.total_size_after))
        result.append('- Saved:                %s (%i b)' % (format_size(self.total_size_before - self.total_size_after), self.total_size_before - self.total_size_after))
        result.append('- Percentage of source: %.2f%%' % (self.total_size_after / ((self.total_size_before / 100) or 1)))

        if self.errors:
            result.append('\nErrors:')

            for error in self.errors:
                result.append('    ' + decode(str(error)))
        else:
            result.append('\nNo errors!')

        return '\n'.join(result)


class Optimizer:
    def __init__(self, files, threads=None, logging=True, resize=False):
        self.files = files
        self.threads = threads or 0
        self.logging = logging
        self.resize_pattern = self._prepare_resize_value(resize)
        self.total_files = len(self.files)
        self.files_count_len = len(str(len(self.files)))
        self.counter = 0
        self.stats = Statistics(self)

    def log(self, value):
        if self.logging:
            logger.info(value)

    @staticmethod
    def _prepare_resize_value(value):
        if isinstance(value, str):
            match = re.search(r'^(?P<flag>(min|max))?(?P<width>\d+)x(?P<height>\d+)(?P<force>f)?$', value)
            if match:
                return ResizePattern(match.group('flag'), int(match.group('width')), int(match.group('height')), bool(match.group('force')))
            raise ImageOptimizerError('Invalid resize pattern.')
        return False

    def run(self):
        if not self.files:
            self.log('No files found...')
            return

        self.stats.elapsed_time = time.time()

        self.log('Files found: %s\n' % self.total_files)

        if self.threads:
            threads = [threading.Thread(target=self.handler) for _ in range(self.threads)]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()
        else:
            self.handler()

        self.stats.elapsed_time = time.time() - self.stats.elapsed_time
        self.show_results()

    def handler(self):
        while self.files:
            self.process_image_file(self.files.pop(0))

    def process_image_file(self, file):
        if not os.path.exists(file):
            self.stats.errors.append(Error(file, 'File not found!'))
            return
        try:
            size_before = os.path.getsize(file)

            self.optimize_image(file)

            self.stats.success.append(file)
            size_after = os.path.getsize(file)
            result = 'OK. [%s (%i b) => %s (%i b)] %.2f%%' % (format_size(size_before), size_before, format_size(size_after), size_after, size_after / (size_before / 100))

            self.stats.total_size_before += size_before
            self.stats.total_size_after += size_after
        except Exception as ex:
            self.stats.errors.append(Error(file, ex))
            result = 'ERROR!'

        self.counter += 1

        self.log(('[%0' + str(self.files_count_len) + 'd/%0' + str(self.files_count_len) + 'd] %s: %s') % (self.counter, self.total_files, decode(file), result))

    def optimize_image(self, path):
        with Image.open(path) as image:
            name, ext = os.path.splitext(os.path.basename(path))

            image = self.process_image(image, ext)

            image.save(os.path.join(os.path.dirname(path), '%s%s' % (name, ext.lower())), optimize=True)

    def process_image(self, image, ext):
        image = self._fix_image_mode(image, ext.strip('.'))

        if self.resize_pattern and self.resize_pattern.has_need_resize(image):
            image = Resizer.resize(image, self.resize_pattern)
            self.stats.resized += 1

        return image

    @staticmethod
    def _fix_image_mode(image, ext):
        if ext in ('jpg', 'jpeg') and image.mode not in ('1', 'L', 'RGB', 'CMYK', 'YCbCr'):
            return image.convert('RGB')
        return image

    def show_results(self):
        self.log(str(self.stats))
