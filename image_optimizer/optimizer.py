import argparse
import os
import sys
import threading
import time
from datetime import datetime

from PIL import Image
from image_optimizer import __version__

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
    def __init__(self, files):
        self.files = files
        self.success = []
        self.errors = []
        self.total_files = len(self.files)
        self.total_size_before = 0
        self.total_size_after = 0
        self.files_count_len = len(str(len(self.files)))
        self.elapsed_time = 0
        self.counter = 0
        self.threads = 0

    def optimize(self, thread_count=0):
        self.elapsed_time = time.time()
        self.threads = thread_count if thread_count else 0

        print('Files found: %s' % self.total_files)

        if self.threads:
            threads = []
            for i in range(self.threads):
                threads.append(threading.Thread(target=self.thread_process))

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
            result = 'OK. [%.2f Kb (%i b) => %.2f Kb (%i b)] %.2f%%' % (size_before / 1024, size_before, size_after / 1024, size_after, size_after / (size_before / 100))
        except Exception as ex:
            self.errors.append(OptimizerError(file, ex))
            result = 'ERROR!'

        self.total_size_before += size_before
        self.total_size_after += size_after
        self.counter += 1

        print(('[%0' + str(self.files_count_len) + 'd/%0' + str(self.files_count_len) + 'd] %s: %s') % (self.counter, self.total_files, decode(file), result))

    def show_total_results(self):
        print('\nOptimization done!\n')
        print('- Elapsed time:         %s' % datetime.utcfromtimestamp(self.elapsed_time).strftime('%H:%M:%S.%f'))
        print('- Thread count:         %s' % (self.threads if self.threads else 1))
        print('- Files optimized:      %s' % len(self.success))
        print('- Size before:          %.2f Kb (%i b)' % (self.total_size_before / 1024, self.total_size_before))
        print('- Size after:           %.2f Kb (%i b)' % (self.total_size_after / 1024, self.total_size_after))
        print('- Saved:                %.2f Kb (%i b)' % ((self.total_size_before - self.total_size_after) / 1024, self.total_size_before - self.total_size_after))
        print('- Percentage of source: %.2f%%' % (self.total_size_after / (self.total_size_before / 100)))

        if self.errors:
            print('\nErrors:')
            for error in self.errors:
                print('\t' + decode(str(error)))
        else:
            print('\nNo errors!')


def main():
    parser = argparse.ArgumentParser(description='PIL image optimizer v%s by Bobsans' % __version__)
    parser.add_argument(dest='source', type=str, help='source to optimize')
    parser.add_argument('-r', dest='recursive', action='store_true', help='recursive scan subfolders')
    parser.add_argument('-t', dest='threads', type=int, help='set thread count')

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
            print('Path not exists!', file=sys.stderr)
    else:
        parser.print_help()
        exit()

    if files:
        Optimizer(files).optimize(args.threads)
    else:
        print('Image files not found...')


if __name__ == '__main__':
    main()
