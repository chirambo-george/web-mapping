from flask import Flask, render_template
import folium
import pandas as pd
import geopandas as gpd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title = 'home')

@app.route('/map')
def map_view():

    cities = pd.read_csv('week-01/geo-web-mapping/data/pop.csv')
    mw_admin = gpd.read_file('week-01/geo-web-mapping/data/mw_admin.geojson')
    # creating a map object 
    m = folium.Map(
        location=[-15.987, 34.840], 
        tiles = 'CartoDB Positron',
        min_zoom = 1
    )

    # creating a marker
    for idx, city in cities.iterrows():
        folium.Marker(
            location = [city['latitude'], city['longitude']],
            tooltip = city['city'],
            popup = f"""
                <b>{city['city']}</b><br>
                Region: {city.get('region', 'N/A')}<br>
                Population: {city['population']:,}
                """,
            icon = folium.Icon(color="green"),
                ).add_to(m)
    
    # Convert Timestamp columns to string
    for col in mw_admin.select_dtypes(include=["datetime64[ns]"]).columns:
        mw_admin[col] = mw_admin[col].astype(str)

    # adding boundary data - mw shapefile

    for idx, dist in mw_admin.iterrows():
        folium.GeoJson(
            mw_admin.to_json(), 
            name = "Malawi Boundaries", 
            tooltip = folium.GeoJson(
                dist["geometry"].__geo_interface__,  # single feature geometry
                name=f"District {dist['adm2_name']}",
                tooltip=dist['adm2_name']
                )
                                            
            ).add_to(m)
    

    # adding layer control option 
    folium.LayerControl().add_to(m)

    # Converting to HTML and rendering 
    map_html = m._repr_html_()
    
    return render_template('map.html', map = map_html)

# 
if __name__ == '__main__':
    app.run(debug=True)