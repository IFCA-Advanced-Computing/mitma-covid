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

import pandas as pd

from utils import PATHS


def fix_1207():
    """
    Fix error in original dataset (see README)
    """
    rawdir = PATHS.rawdir / 'maestra1' / 'municipios'
    src = rawdir / '20200705_maestra_1_mitma_municipio.txt.gz'
    dst = rawdir / '20200712_maestra_1_mitma_municipio.txt.gz'

    df = pd.read_csv(src,
                     sep='|',
                     thousands='.',
                     dtype={'origen': 'string', 'destino': 'string'},
                     compression='gzip')

    # Replace date
    df['fecha'] = '20200712'

    # Apply thousands separator
    def add_sep(x):
        x = str(x)
        if len(x) > 3:
            return f'{str(x)[:-3]}.{str(x)[-3:]}'
        else:
            return x

    df['viajes'] = df['viajes'].apply(add_sep)
    df['viajes_km'] = df['viajes_km'].apply(add_sep)

    df.to_csv(dst,
              sep='|',
              compression='gzip',
              index=False)
