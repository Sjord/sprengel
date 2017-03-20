from __future__ import print_function
import requests
import sys
import os
import os.path
import subprocess

files = [
    '.hg/store/00manifest.i',
    '.hg/store/00manifest.d',
    '.hg/store/00changelog.i',
    '.hg/store/00changelog.d',
    '.hg/dirstate',
    '.hg/requires',
    '.hg/hgrc',
]


def urljoin(a, b):
    return a + '/' + b

def save_file(url, path):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass

    response = requests.get(url)
    if response.ok:
        with open(path, 'wb') as fp:
            fp.write(response.content)
        print('OK: ', path)
    else:
        print('FAIL: ', path)


def encode_path(filename):
    # TODO do case folding
    return filename.replace('_', '__')

if __name__ == "__main__":
    host = sys.argv[1]

    for f in files:
        url = urljoin(host, f)
        save_file(url, f)

    manifest = subprocess.check_output(['hg', '--debug', 'manifest'])
    for line in manifest.split('\n'):
        filename = line[47:]
        encoded = encode_path(filename)
        for f in ['.hg/store/data/%s.i', '.hg/store/data/%s.d']:
            url = urljoin(host, f % encoded)
            save_file(url, f % filename)


