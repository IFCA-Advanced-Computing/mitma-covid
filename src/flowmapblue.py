"""
Generate the files for flowmap blue of existing processed files

Add the following to the map url to customize it nicely
?f=13&col=BurgYl&c=0&bo=100

Play with params here:
f: fade transparency, c: clustering, col: color, bo: base map transparency
https://flowmap.blue/1mK1ZMxNmGtSSxMhtoKO5h7nxyDMXFC_3_u4eo4rtucg/ce149d3?v=45.533556,-73.600797,10.87,0,0&a=0&as=1&b=1&bo=100&c=0&ca=1&d=1&fe=1&lt=1&lfm=ALL&col=BurgYl&f=13
"""

import requests
import pandas as pd

from utils import PATHS

# todo: Add integration with Google Spreadsheets
# Upload csv to Google spreadsheets to be able to divide it in months
# Flowmap will run more smoothly


def generate_flowmapblue():

    flows = pd.read_csv(PATHS.processed / "province_flux.csv")

    # Load coordinates of places
    f = PATHS.processed / "flowmap-blue" / "coord.csv"
    if not f.exists():
        lat, lon = [], []
        names = sorted(set(flows['province origin']))
        for province in names:
            url = 'https://nominatim.openstreetmap.org/search'
            if province in ['Ceuta', 'Melilla']:
                params = {'city': province, 'country': 'spain', 'format': 'json'}
            else:
                params = {'county': province, 'country': 'spain', 'format': 'json'}
            r = requests.get(url, params=params)
            r = r.json()[0]
            lat.append(r['lat'])
            lon.append(r['lon'])

        coord = pd.DataFrame({'name': names, 'lat': lat, 'lon': lon})
        coord.to_csv(
            PATHS.processed / "flowmap-blue" / "coord.csv",
            index=False,
        )
    else:
        coord = pd.read_csv(f)

    # Save locations
    locations = flows.groupby(['province origin', 'province id origin']).size().reset_index()
    locations = locations.drop(0, axis=1)
    locations = locations.rename(columns={"province origin": "name", "province id origin": "id"})
    locations = locations.merge(coord)
    locations = locations[['id', 'name', 'lat', 'lon']]

    locations.to_csv(
        PATHS.processed / "flowmap-blue" / "locations.csv",
        index=False,
    )

    # Save flows
    flows = flows.rename(columns={"province id origin": "origin",
                                  "province id destination": "dest",
                                  "flux": "count",
                                  "date": "time"})
    flows = flows.drop(['province origin', 'province destination'], axis=1)

    flows.to_csv(
        PATHS.processed / "flowmap-blue" / "flows.csv",
        index=False,
    )


if __name__ == '__main__':
    generate_flowmapblue()
