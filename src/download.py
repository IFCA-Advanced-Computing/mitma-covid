# Copyright (c) 2020 Spanish National Research Council
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import urllib.parse
import datetime

from tqdm import tqdm
import requests
import pandas as pd

from utils import PATHS

BASE_URL = 'https://opendata-movilidad.mitma.es'


def download(exp='maestra1',
             res='municipios',
             update=False,
             force=False):

    # Prepare output dir
    files = []
    rawdir = PATHS.rawdir / f'{exp}' / f'{res}'
    rawdir.exists() or os.makedirs(rawdir)

    # Generate time range
    lsfiles = sorted(os.listdir(rawdir))
    if update:
        start = datetime.datetime.strptime(lsfiles[-1][:8], '%Y%m%d').date()
        start += datetime.timedelta(days=1)
    else:
        start = datetime.date(2020, 2, 21)
    end = datetime.datetime.today().date()
    dates = pd.date_range(start, end, freq='d')

    if dates.empty:
        print('Already up-to-date')
        return []

    # Download files
    print(f'Downloading files for the period {start} - {end}')
    s = requests.Session()
    for d in tqdm(dates):
        url = f'{BASE_URL}/{exp}-mitma-{res}/ficheros-diarios/{d:%Y}-{d:%m}/{d:%Y%m%d}_maestra_{exp[-1]}_mitma_{res[:-1]}.txt.gz'

        aux = urllib.parse.urlparse(url)
        fpath = os.path.basename(aux.path)
        fpath = rawdir / fpath

        if fpath.exists() and not force:
            print(f"\t {os.path.basename(url)} already downloaded, not overwriting it."
                   " To overwrite it use (force=True)")
            continue

        try:
            resp = s.get(url)
            if resp.status_code == 404:
                print(f'{d.date()} not available yet')
                continue
            with open(fpath, 'wb') as f:
                f.write(resp.content)
            files.append(fpath)

        except Exception as e:
            print(f'Error downloading {url}')

    return files


if __name__ == '__main__':
    download()
