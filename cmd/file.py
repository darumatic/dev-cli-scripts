import argparse
import os
import re
import sys


def find(dir, name, content):
    if dir is None:
        dir = os.getcwd()

    name_pattern = None
    if name is not None:
        name_pattern = re.compile(name.replace("*", ".*"))

    content_pattern = None
    if content is not None:
        content_pattern = re.compile(content.replace("*", ".*"), re.MULTILINE)

    if name_pattern is None and content_pattern is None:
        print("Need at least specify name or content")
        exit(1)

    count = 0
    package_files = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            lower_name = name.lower()
            if name_pattern is not None and not name_pattern.search(lower_name):
                continue

            file = os.path.join(root, name)
            if content_pattern is not None:
                with open(file, 'r') as f:
                    content = f.read()
                    print(content)
                    if not content_pattern.search(content):
                        continue

            print(file)
            count += 1

    print('found {}'.format(count))
    return package_files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='file')
    subparsers = parser.add_subparsers(help='find file', dest='action')

    find_parser = subparsers.add_parser('find', help='Find files')
    find_parser.add_argument('--dir', type=str, required=False)
    find_parser.add_argument('--name', type=str, required=False)
    find_parser.add_argument('--content', type=str, required=False)

    options, argv = parser.parse_known_args(sys.argv[1:])
    action = options.action

    if action == 'find':
        find(options.dir, options.name, options.content)
        exit(0)
    else:
        parser.print_help()
        exit(1)
