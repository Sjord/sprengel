from __future__ import print_function, unicode_literals
import requests
import sys
import os
import os.path
import subprocess


# Files that exist in any Mercurial repository
base_files = [
    '.hg/store/00manifest.i',
    '.hg/store/00manifest.d',
    '.hg/store/00changelog.i',
    '.hg/store/00changelog.d',
    '.hg/store/fncache',
    '.hg/dirstate',
    '.hg/requires',
    '.hg/hgrc',
    '.hg/last-message.txt',
]


def urljoin(a, b):
    return a.rstrip('/') + '/' + b.lstrip('/')


def save_file(url, path):
    print("%-60s" % path, end='')
    if os.path.isfile(path):
        print("-")
        return

    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass

    response = requests.get(url)
    if response.ok:
        with open(path, 'wb') as fp:
            fp.write(response.content)

    print(response.status_code)


def encode_char(c):
    try:
        cord = c
        cchr = chr(c)
    except:
        cord = ord(c)
        cchr = c

    if cord >= 126 or cchr in '\:*?"<>|':
        return '~%x' % cord
    if cchr.isupper():
        return '_' + cchr.lower()
    if cchr == '_':
        return '__'
    return cchr


def encode_path(filename):
    return ''.join([encode_char(c) for c in filename])


def download_base_files(host):
    for f in base_files:
        url = urljoin(host, f)
        save_file(url, f)


def get_manifest_file_list():
    manifest = subprocess.check_output(['hg', '--debug', 'manifest'])
    files = []
    for line in manifest.split(b'\n'):
        if line:
            files.append(line[47:])
    return files


def download_manifest_files(files):
    for filename in files:
        encoded = encode_path(filename)
        for f in ['.hg/store/data/%s.i', '.hg/store/data/%s.d']:
            url = urljoin(host, f % encoded)
            save_file(url, f % encoded)


def download_hg_directory(host):
    download_base_files(host)
    files = get_manifest_file_list()
    download_manifest_files(files)


if __name__ == "__main__":
    try:
        host = sys.argv[1]
        download_hg_directory(host)
        print("""
        Downloaded files into .hg directory.
        Run 'hg verify' to check the integrity of the repository.
        Run 'hg update -C' to restore files.
        """)
    except IndexError:
        print("Usage: %s http://example.com/", sys.argv[0])
