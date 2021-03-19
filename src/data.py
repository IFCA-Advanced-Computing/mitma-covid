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

import click

from download import download
from flowmapblue import generate_flowmapblue
from misc import fix_1207

from process import process


@click.command()
@click.option('--update', '-u', is_flag=True, help="Update current files without overwriting.")
def data(update):
    if update:
        print('Updating the existing files')
    else:
        print('Generating data from scratch')

    files = download(exp='maestra1',
                     res='municipios',
                     update=update,
                     force=False)
    fix_1207()
    process(day_files=files,
            exp='maestra1',
            res='municipios',
            update=update,
            force=False)
    generate_flowmapblue()


if __name__ == '__main__':
    data()
