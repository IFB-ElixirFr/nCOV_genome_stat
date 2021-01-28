import json

with open('home/static/data/countries.geojson') as f:
  data = json.load(f)


data['features'][0]['geometry']