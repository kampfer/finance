# coding: utf-8

import sys
import time
import requests
from tqdm import tqdm
import json

def download(targetUrl):
    initUrl = 'https://www.gold.org/wgc/ajax/with_price/'
    loginUrl = 'https://www.gold.org/wgc/ajax/login/'
    # targetUrl = 'http://www.gold.org/download/file/2977/Prices.xls'
    # targetUrl = 'http://www.gold.org/download/file/5559/Gold-backed-ETF-data-ZH.xlsx'

    s = requests.session()

    r = s.post(initUrl, data={
        'referer': 'http://www.gold.org/cn/homepage',
        'href': 'http://www.gold.org/cn/page/4699#tab5',
        'nid': 4699,
        'return_url': 'http://www.gold.org/cn/page/4699#tab5'
    }, verify=False)
    tokenValue = json.loads(r.content)['token_value']

    r = s.post(loginUrl, data={
        'email': '2258287411@qq.com',
        'password': '123qwe',
        'curr_lang': 'chinese',
        'wgc_csrf': tokenValue
    }, verify=False)

    r = s.get(targetUrl, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    filename = time.strftime('%Y-%m-%d', time.localtime()) + '.xlsx'
    with open(filename, 'wb') as f:
        for data in tqdm(r.iter_content(), total=total_size, unit='B', unit_scale=True, leave=True):
            f.write(data)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        targetUrl = sys.argv[2]
    else:
        targetUrl = 'http://www.gold.org/download/file/3022/Prices.xlsx'

    download(targetUrl)
