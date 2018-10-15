import argparse
import os
import sys

from image_optimizer import FORMATS, __version__
from image_optimizer.errors import ImageOptimizerError
from image_optimizer.optimizer import Optimizer


class OptimizerWrapper(Optimizer):
    pass


def main():
    parser = argparse.ArgumentParser(description='PIL image optimizer v%s by Bobsans' % __version__)
    parser.add_argument(dest='source', type=str, help='source to optimize')
    parser.add_argument('-r', dest='recursive', action='store_true', help='recursive scan subfolders')
    parser.add_argument('-t', dest='threads', type=int, help='set thread count')
    parser.add_argument('-l', dest='logging', action='store_false', help='disable logging')
    parser.add_argument('-s', dest='resize_pattern', action='store', help='resize images')

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
                            if ext and ext.lower()[1:] in FORMATS:
                                files.append(os.path.join(r, file))
                else:
                    for file in os.listdir(args.source):
                        name, ext = os.path.splitext(file)
                        if ext and ext.lower()[1:] in FORMATS:
                            files.append(os.path.join(args.source, file))
        else:
            sys.stderr.write('\nPath not exists!\n')
    else:
        parser.print_help()
        exit()

    optimizer = Optimizer(files, args.threads, args.logging, args.resize_pattern)

    try:
        optimizer.run()
    except KeyboardInterrupt:
        sys.stdout.write('\nInterrupted by keyboard.\n')
        optimizer.show_results()
    except ImageOptimizerError as e:
        sys.stderr.write('\n' + str(e) + '\n')

main()