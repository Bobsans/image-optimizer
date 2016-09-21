import argparse
import os
import sys
from PIL import Image

__author__ = 'Bobsans'
__version__ = '0.2b1'

PIL_FORMATS = [
    'bmp', 'eps', 'gif', 'icns', 'im', 'jpeg', 'jpg', 'jpe', 'jfif', 'j2k', 'j2p',
    'jpx', 'msp', 'pcx', 'png', 'ppm', 'spi', 'tiff', 'tif', 'webp', 'xbm', 'xv'
]


def decode_path(path):
    return path.encode(sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding)


def main():
    parser = argparse.ArgumentParser(description='PIL image optimizer v%s by %s.' % (__version__, __author__))
    parser.add_argument('-f', action='store', nargs='+', dest='files', help='files to optimize')
    parser.add_argument('-d', action='store', dest='folder', help='folder to optimize')
    parser.add_argument('--sub', action='store_true', dest='subfolders', help='scan subdirectories')

    args = parser.parse_args()

    files = []
    errors = []
    before = 0
    after = 0
    count = 0
    current = 1

    if args.files:
        files = args.files
    elif args.folder and os.path.exists(args.folder):
        if args.subfolders:
            for r, d, f in os.walk(args.folder):
                for file in f:
                    name, ext = os.path.splitext(file)
                    if ext and ext.lower()[1:] in PIL_FORMATS:
                        files.append(os.path.join(r, file))
        else:
            for file in os.listdir(args.folder):
                name, ext = os.path.splitext(file)
                if ext and ext.lower()[1:] in PIL_FORMATS:
                    files.append(os.path.join(args.folder, file))
    else:
        parser.print_help()
        exit()

    if files:
        print('Files found: %s' % len(files))
        files_count_len = str(len(str(len(files))))
        for file in files:
            if os.path.exists(file):
                print(('Processing file [%0' + files_count_len + 'd/%0' + files_count_len + 'd] "%s"... ') % (current, len(files), decode_path(file)), end='')
                try:
                    before += os.path.getsize(file)
                    with Image.open(file) as img:
                        name, ext = os.path.splitext(os.path.basename(file))
                        img.save(os.path.join(os.path.dirname(file), '%s%s' % (name, ext.lower())), optimize=True)
                    count += 1
                except Exception as e:
                    print('ERROR')
                    errors.append({'file': file, 'exception': e})
                else:
                    print('OK')
                    after += os.path.getsize(file)
                current += 1

        print('\nCompressing done!\n')
        print('- Files compressed:   %s' % count)
        print('- Before size:        %.2f Kb (%i b)' % (before / 1024, before))
        print('- After size:         %.2f Kb (%i b)' % (after / 1024, after))
        print('- Saved               %.2f Kb (%i b)' % ((before - after) / 1024, before - after))
        print('- Percents of source: %.2f%%' % (after / (before / 100)))

        if errors:
            print('\nError files:')
            for f in errors:
                print('    %s: %s' % (decode_path(f.get('file')), f.get('exception')))
    else:
        print('Image files not found...')


if __name__ == '__main__':
    main()
