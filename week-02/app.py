import folium, geopandas
from flask import Flask, render_template

# initializing a Flask object
app = Flask(__name__)

# configuring routes
@app.route('/')
def index():
    return render_template('index.html', title = 'home page')

# map view 
@app.route('/map')
def map_view():

    mw_boundary =  geopandas.read_file('week-01/geo-web-mapping/data/mw_admin.geojson')
    # initializing map object / { the basemap }
    m = folium.Map(
        location = [-13.983, 33.783],
        tiles = "CartoDB Positron",
        zoom_start  = 7
    )
    # Convert Timestamp columns to string
    for col in mw_boundary.select_dtypes(include=["datetime64[ns]"]).columns:
        mw_boundary[col] = mw_boundary[col].astype(str)
        
    # adding a geojson layer 
    folium.GeoJson(
        mw_boundary.to_json(),
        name = "MW Admin Boundary",
        style_function=lambda x: {
            'color':"#b4b2b2", 'weight':2  },
        tooltip = folium.GeoJsonTooltip(
            fields=['adm2_name'],
            aliases = ['District:']
            
        ),
        popup = folium.GeoJsonPopup(
            fields=['adm1_name', 'adm2_name'], 
            aliases=['Region:', 'District:']
        ),
        highlight_function=lambda feature: {
            'weight': 3,
            'color': "#b4474792", # Change to red on hover/click instead of black
            'fillColor': "#00ffff92"
        }
    ).add_to(m)

    # Converting to HTML and rendering 
    map_html = m._repr_html_()
    return render_template('map.html', map = map_html)


if __name__ == '__main__':
    app.run(debug=True)