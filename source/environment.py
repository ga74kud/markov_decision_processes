from flask import Flask
import overpy
import folium as fm
import json

api = overpy.Overpass()
result = api.query("node(47.030089,15.427316,47.030665,15.429228);out;")

m = fm.Map(location=[45.5236, -122.6750])

for wlt in result.nodes:
    abc=(wlt.lat, wlt.lon, wlt.tags)
    b=1


with open('../input/puntigam.json') as json_file:
    data = json.load(json_file)
    abc=1
app = Flask(__name__)
@app.route('/')
def index():
    start_coords = (47.030089, 15.427316)

    m = fm.Map(
        location=start_coords,
        tiles='Stamen Toner',
        zoom_start=30)

    tooltip = 'Click me!'
    for idx, qrt in enumerate(data):
        fm.Marker(data[qrt], popup='<i>Mt. Hood Meadows</i>', tooltip=tooltip).add_to(m)

    return m._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
