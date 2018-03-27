import argparse
import os
import sys
import threading
import time
from datetime import datetime

from PIL import Image

from image_optimizer import __version__
from image_optimizer.utils import format_size

PIL_FORMATS = [
    'bmp', 'eps', 'gif', 'j2c', 'j2k', 'jp2', 'jpc', 'jpe', 'jpeg', 'jpf', 'jpg', 'jpx', 'mpo', 'pbm',
    'pcx', 'pgm', 'png', 'ppm', 'tga'
]


def decode(path):
    return path.encode(sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding)


class OptimizerError:
    def __init__(self, file, error):
        self.file = file
        self.type = error.__class__.__name__ if isinstance(error, Exception) else 'OptimizeError'
        self.message = str(error)

    def __str__(self):
        return '%s [%s: %s]' % (self.file, self.type, self.message)


class Optimizer:
    def __init__(self, files, threads=1, logging=True):
        self.files = files
        self.threads = threads or 0
        self.logging = logging
        self.success = []
        self.errors = []
        self.total_files = len(self.files)
        self.total_size_before = 0
        self.total_size_after = 0
        self.files_count_len = len(str(len(self.files)))
        self.elapsed_time = 0
        self.counter = 0
        self.threads = 0

    def log(self, value):
        if self.logging:
            print(value)

    def optimize(self):
        if not self.files:
            self.log('No files found...')
            return

        self.elapsed_time = time.time()

        self.log('Files found: %s' % self.total_files)

        if self.threads:
            threads = [threading.Thread(target=self.thread_process) for _ in range(self.threads)]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()
        else:
            self.thread_process()

        self.elapsed_time = time.time() - self.elapsed_time
        self.show_total_results()

    def thread_process(self):
        while self.files:
            self.process_image_file(self.files.pop(0))

    def process_image_file(self, file):
        size_before = 0
        size_after = 0

        if not os.path.exists(file):
            self.errors.append(OptimizerError(file, 'File not found!'))
            return
        try:
            size_before = os.path.getsize(file)
            with Image.open(file) as img:
                name, ext = os.path.splitext(os.path.basename(file))
                img.save(os.path.join(os.path.dirname(file), '%s%s' % (name, str(ext).lower())), optimize=True)
            self.success.append(file)
            size_after = os.path.getsize(file)
            result = 'OK. [%s (%i b) => %s (%i b)] %.2f%%' % (format_size(size_before), size_before, format_size(size_after), size_after, size_after / (size_before / 100))

            self.total_size_before += size_before
            self.total_size_after += size_after
        except Exception as ex:
            self.errors.append(OptimizerError(file, ex))
            result = 'ERROR!'

        self.counter += 1

        self.log(('[%0' + str(self.files_count_len) + 'd/%0' + str(self.files_count_len) + 'd] %s: %s') % (self.counter, self.total_files, decode(file), result))

    def show_total_results(self):
        self.log('\nOptimization done!\n')
        self.log('- Elapsed time:         %s' % datetime.utcfromtimestamp(self.elapsed_time).strftime('%H:%M:%S.%f'))
        self.log('- Thread count:         %s' % (self.threads if self.threads else 1))
        self.log('- Files optimized:      %s' % len(self.success))
        self.log('- Size before:          %s (%i b)' % (format_size(self.total_size_before), self.total_size_before))
        self.log('- Size after:           %s (%i b)' % (format_size(self.total_size_after), self.total_size_after))
        self.log('- Saved:                %s (%i b)' % (format_size(self.total_size_before - self.total_size_after), self.total_size_before - self.total_size_after))
        self.log('- Percentage of source: %.2f%%' % (self.total_size_after / (self.total_size_before / 100)))

        if self.errors:
            self.log('\nErrors:')
            for error in self.errors:
                self.log('\t' + decode(str(error)))
        else:
            self.log('\nNo errors!')


def main():
    parser = argparse.ArgumentParser(description='PIL image optimizer v%s by Bobsans' % __version__)
    parser.add_argument(dest='source', type=str, help='source to optimize')
    parser.add_argument('-r', dest='recursive', action='store_true', help='recursive scan subfolders')
    parser.add_argument('-t', dest='threads', type=int, help='set thread count')
    parser.add_argument('-l', dest='logging', action='store_false', help='disable logging')

    args = parser.parse_args()

    files = []

    if args.source:
        if os.path.exists(args.source):
            if os.path.isfile(args.source):
                files.append(args.source)
            elif os.path.isdir(args.source):
                if args.recursive:
                    for r, d, f in os.walk(args.source):
                        for file in f:
                            name, ext = os.path.splitext(file)
                            if ext and ext.lower()[1:] in PIL_FORMATS:
                                files.append(os.path.join(r, file))
                else:
                    for file in os.listdir(args.source):
                        name, ext = os.path.splitext(file)
                        if ext and ext.lower()[1:] in PIL_FORMATS:
                            files.append(os.path.join(args.source, file))
        else:
            print('Path not exists!')
    else:
        parser.print_help()
        exit()

    Optimizer(files, args.threads, args.logging).optimize()


if __name__ == '__main__':
    main()
