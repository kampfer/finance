# coding: utf-8

import sys
import time
import requests
from tqdm import tqdm

def download(file):
    filename = time.strftime('%Y-%m-%d', time.localtime()) + '.xlsx'
    print(filename)

    r = requests.get(file)
    total_size = int(r.headers.get('content-length', 0))

    with open(filename, 'wb') as f:
        for data in tqdm(r.iter_content(32*1024), total=total_size, unit='B', unit_scale=True):
            f.write(data)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        targetUrl = sys.argv[2]
    else:
        targetUrl = 'http://www.gold.org/download/file/3022/Prices.xlsx'

    download(targetUrl)
