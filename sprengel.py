from __future__ import print_function
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
    '.hg/dirstate',
    '.hg/requires',
    '.hg/hgrc',
    '.hg/last-message.txt',
]


def urljoin(a, b):
    return a + '/' + b

def save_file(url, path):
    if os.path.isfile(path):
        print("SKIP: ", path)
        return

    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass

    response = requests.get(url)
    if response.ok:
        with open(path, 'wb') as fp:
            fp.write(response.content)
        print('OK:   ', path)
    else:
        print('FAIL: ', path)


def encode_char(c):
    if c == '_':
        return '__'
    if c.isupper():
        return '_' + c.lower()
    if ord(c) >= 126 or c in '\:*?"<>|':
        return '~%x' % ord(c)
    return c


def encode_path(filename):
    return ''.join([encode_char(c) for c in filename])


def download_base_files(host):
    for f in base_files:
        url = urljoin(host, f)
        save_file(url, f)


def get_manifest_file_list():
    manifest = subprocess.check_output(['hg', '--debug', 'manifest'])
    files = []
    for line in manifest.split('\n'):
        if line:
            files.append(line[47:])
    return files


def download_manifest_files(files):
    for filename in files:
        encoded = encode_path(filename)
        print(encoded)
        for f in ['.hg/store/data/%s.i', '.hg/store/data/%s.d']:
            url = urljoin(host, f % encoded)
            save_file(url, f % filename)


def download_hg_directory(host):
    download_base_files(host)
    files = get_manifest_file_list();
    download_manifest_files(files)


if __name__ == "__main__":
    try:
        host = sys.argv[1]
        download_hg_directory(host)
    except IndexError:
        print("Usage: %s http://example.com/", sys.argv[0])
