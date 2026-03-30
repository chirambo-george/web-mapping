# WEEK 3: Spatial Analysis & Choropleth Mapping

**Phase:** Foundations (Days 1–20)  
**Target Hours:** 15–20 hrs/week  
**Focus:** Spatial operations (buffer, intersect), choropleth maps, advanced filtering

---

## Daily Breakdown

### Day 11: GeoPandas Spatial Operations

**Morning (2–3 hrs):**
- [ ] Learn GeoPandas spatial operations: buffer, intersect, dissolve, centroid
- [ ] Understand projection systems (EPSG codes)
- [ ] Practice with sample Malawi data

**Resources:**
- GeoPandas Spatial Operations: https://geopandas.org/docs/user_guide/geometric_operations.html

**Code (`geo_utils/spatial_ops.py` - new file):**
```python
import geopandas as gpd
from shapely.geometry import box, Point
import pandas as pd

def load_shapefile(filepath):
    """Load shapefile as GeoDataFrame"""
    return gpd.read_file(filepath)

def buffer_geometry(gdf, distance_m):
    """Buffer geometries by distance in meters
    
    Args:
        gdf: GeoDataFrame
        distance_m: buffer distance in meters
    
    Returns:
        GeoDataFrame with buffered geometries
    """
    gdf_copy = gdf.copy()
    # If in lat/lon, convert to projected CRS first
    if gdf.crs.to_epsg() in [4326, 4267]:  # lat/lon codes
        gdf_copy = gdf_copy.to_crs('EPSG:3857')  # Web Mercator
    
    gdf_copy['geometry'] = gdf_copy.geometry.buffer(distance_m)
    return gdf_copy

def spatial_intersect(gdf, geometry):
    """Find features intersecting a geometry
    
    Args:
        gdf: GeoDataFrame
        geometry: Shapely geometry to intersect with
    
    Returns:
        GeoDataFrame of intersecting features
    """
    return gdf[gdf.geometry.intersects(geometry)]

def spatial_within(gdf, geometry):
    """Find features completely within a geometry"""
    return gdf[gdf.geometry.within(geometry)]

def dissolve_by_property(gdf, dissolve_col):
    """Dissolve boundaries by property (e.g., combine districts into regions)
    
    Args:
        gdf: GeoDataFrame
        dissolve_col: Column name to dissolve by
    
    Returns:
        GeoDataFrame with dissolved boundaries
    """
    return gdf.dissolve(by=dissolve_col, aggfunc='sum')

def calculate_centroids(gdf):
    """Calculate centroid of each geometry"""
    gdf_copy = gdf.copy()
    gdf_copy['centroid'] = gdf_copy.geometry.centroid
    return gdf_copy

def nearest_feature(gdf, geometry, n=1):
    """Find n nearest features to a geometry"""
    gdf_copy = gdf.copy()
    gdf_copy['distance'] = gdf_copy.geometry.distance(geometry)
    return gdf_copy.nsmallest(n, 'distance')

def intersect_two_layers(gdf1, gdf2):
    """Spatial join: find overlaps between two layers"""
    return gpd.sjoin(gdf1, gdf2, how='inner', predicate='intersects')

def reproject_to_utm(gdf):
    """Convert lat/lon to UTM (South Africa/Malawi zone 35/36)"""
    # Malawi is in UTM zone 35S and 36S
    return gdf.to_crs('EPSG:32735')  # UTM 35S
```

**Afternoon (2–3 hrs):**
- [ ] Test spatial operations with Malawi data
- [ ] Create test script to verify operations work
- [ ] Document expected outputs

**Code (`test_spatial.py` - for testing):**
```python
import geopandas as gpd
from geo_utils.spatial_ops import (
    buffer_geometry, spatial_intersect, dissolve_by_property,
    calculate_centroids, nearest_feature
)
import json

# Load Malawi districts
gdf = gpd.read_file('data/malawi_districts.geojson')

print("=== Original Data ===")
print(f"Shape: {gdf.shape}")
print(f"CRS: {gdf.crs}")
print(f"Columns: {gdf.columns.tolist()}")

# Test 1: Buffer
print("\n=== Buffer Test (5km) ===")
buffered = buffer_geometry(gdf, 5000)
print(f"Buffered geometries created: {len(buffered)}")

# Test 2: Dissolve (combine districts into regions)
print("\n=== Dissolve Test (by region) ===")
dissolved = dissolve_by_property(gdf, 'region')
print(f"Original: {len(gdf)} districts → Dissolved: {len(dissolved)} regions")
print(dissolved[['region', 'geometry']])

# Test 3: Centroids
print("\n=== Centroid Test ===")
with_centroids = calculate_centroids(gdf)
print(with_centroids[['name', 'centroid']].head())

# Test 4: Intersect with custom point
from shapely.geometry import Point
lilongwe = Point(33.7741, -13.9626)
near_lilongwe = spatial_intersect(gdf, lilongwe.buffer(0.1))
print(f"\n=== Features near Lilongwe ===")
print(near_lilongwe[['name', 'region']])

print("\n✓ All tests passed!")
```

**Run tests:**
```bash
python test_spatial.py
```

**End of Day 11:**
- [ ] Commit to GitHub: "Add spatial operations utility module"
- [ ] test_spatial.py runs without errors
- [ ] Understand GeoPandas spatial methods

---

### Day 12: Choropleth Maps (Color by Attribute)

**Morning (2–3 hrs):**
- [ ] Learn what choropleth maps are (color regions by data attribute)
- [ ] Understand how Folium creates choropleth
- [ ] Plan what data to visualize (population density, literacy rate, etc.)

**Research:**
- Folium Choropleth: https://python-visualization.github.io/folium/latest/user_guide/GeoData.html

**Code (`app.py` - add new route):**
```python
from flask import Flask, render_template, request
import folium
import geopandas as gpd
import json
import os

# ... existing code ...

@app.route('/choropleth')
def choropleth_map():
    """Display choropleth map colored by population"""
    
    # Load data
    geojson_path = 'data/malawi_districts.geojson'
    gdf = gpd.read_file(geojson_path)
    
    # Create map centered on Malawi
    m = folium.Map(
        location=[-13.3, 34.3],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Create choropleth
    folium.Choropleth(
        geo_data=gdf.to_json(),
        name='Population Density',
        data=gdf[['name', 'population']],
        columns=['name', 'population'],
        key_on='feature.properties.name',
        fill_color='YlOrRd',  # Yellow-Orange-Red
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Population',
        nan_fill_color='white'
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add popups with district info
    for idx, row in gdf.iterrows():
        centroid = row.geometry.centroid
        folium.Popup(
            f"<b>{row['name']}</b><br>Population: {row['population']:,}",
            max_width=250
        ).add_to(
            folium.CircleMarker(
                location=[centroid.y, centroid.x],
                radius=0,  # Invisible marker, just for popup
                popup=True
            ).add_to(m)
        )
    
    map_html = m._repr_html_()
    
    return render_template('choropleth.html', map=map_html)
```

**Afternoon (2–3 hrs):**
- [ ] Create template for choropleth map
- [ ] Add legend explaining color scale
- [ ] Test map displays correctly

**Code (`templates/choropleth.html`):**
```html
{% extends "base.html" %}

{% block content %}
<h1>Malawi Population by District</h1>

<div style="display: flex; gap: 20px; margin-bottom: 20px;">
    <div style="flex: 1;">
        <p>This choropleth map shows the population distribution across Malawi districts.</p>
        <p><strong>Color Scale:</strong> Lighter = Lower Population | Darker = Higher Population</p>
    </div>
    
    <div style="background: #f5f5f5; padding: 15px; border-radius: 8px;">
        <h4>Legend</h4>
        <div style="display: flex; flex-direction: column; gap: 5px;">
            <div><span style="background: #FFFFCC; width: 20px; height: 20px; display: inline-block;"></span> Low</div>
            <div><span style="background: #FED98E; width: 20px; height: 20px; display: inline-block;"></span> Low-Medium</div>
            <div><span style="background: #FE9929; width: 20px; height: 20px; display: inline-block;"></span> Medium-High</div>
            <div><span style="background: #EC7014; width: 20px; height: 20px; display: inline-block;"></span> High</div>
            <div><span style="background: #800026; width: 20px; height: 20px; display: inline-block;"></span> Very High</div>
        </div>
    </div>
</div>

<div style="height: 600px; border: 1px solid #ccc; border-radius: 8px; overflow: hidden;">
    {{ map | safe }}
</div>

<p style="margin-top: 20px; font-size: 12px; color: #666;">
    Data source: Malawi Census, GADM administrative boundaries
</p>
{% endblock %}
```

**End of Day 12:**
- [ ] Commit to GitHub: "Add choropleth map route and template"
- [ ] Choropleth displays correctly with color scale
- [ ] Popups show on click

---

### Day 13: Multiple Choropleth Layers (Dynamic Switching)

**Morning (2–3 hrs):**
- [ ] Learn how to create multiple choropleth layers
- [ ] Implement layer switching with buttons/dropdown
- [ ] Calculate different statistics (population, literacy, healthcare access)

**Code (`app.py` - enhanced choropleth route):**
```python
@app.route('/choropleth')
def choropleth_map():
    """Display choropleth with selectable indicators"""
    
    # Get indicator from URL parameter
    indicator = request.args.get('indicator', 'population')
    
    # Load data
    geojson_path = 'data/malawi_districts.geojson'
    gdf = gpd.read_file(geojson_path)
    
    # Define available indicators
    indicators = {
        'population': {
            'column': 'population',
            'title': 'Population',
            'color_scale': 'YlOrRd'
        },
        'literacy': {
            'column': 'literacy_rate',  # Assumes this column exists
            'title': 'Literacy Rate (%)',
            'color_scale': 'YlGn'
        },
        'healthcare': {
            'column': 'healthcare_access',
            'title': 'Healthcare Access (%)',
            'color_scale': 'Blues'
        }
    }
    
    # Validate indicator
    if indicator not in indicators:
        indicator = 'population'
    
    ind_config = indicators[indicator]
    
    # Create map
    m = folium.Map(
        location=[-13.3, 34.3],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Create choropleth with selected indicator
    folium.Choropleth(
        geo_data=gdf.to_json(),
        name=ind_config['title'],
        data=gdf[['name', ind_config['column']]],
        columns=['name', ind_config['column']],
        key_on='feature.properties.name',
        fill_color=ind_config['color_scale'],
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=ind_config['title'],
        nan_fill_color='white'
    ).add_to(m)
    
    folium.LayerControl().add_to(m)
    map_html = m._repr_html_()
    
    return render_template(
        'choropleth.html',
        map=map_html,
        indicator=indicator,
        indicators=indicators.keys(),
        title=ind_config['title']
    )
```

**Afternoon (2–3 hrs):**
- [ ] Update template with indicator selector
- [ ] Add buttons to switch between indicators
- [ ] Test switching between different choropleth maps

**Code (`templates/choropleth.html` - updated):**
```html
{% extends "base.html" %}

{% block content %}
<h1>Malawi Thematic Map</h1>

<div style="margin-bottom: 20px;">
    <label><strong>Select Indicator:</strong></label>
    <div style="display: flex; gap: 10px; margin-top: 10px;">
        {% for ind in indicators %}
            <a href="/choropleth?indicator={{ ind }}" 
               style="
                   padding: 8px 15px;
                   background: {% if ind == indicator %}#667eea{% else %}#ddd{% endif %};
                   color: {% if ind == indicator %}white{% else %}black{% endif %};
                   text-decoration: none;
                   border-radius: 4px;
                   cursor: pointer;
                   transition: all 0.3s;
               "
               onmouseover="this.style.background='#667eea'; this.style.color='white';"
               onmouseout="this.style.background='{% if ind == indicator %}#667eea{% else %}#ddd{% endif %}'; this.style.color='{% if ind == indicator %}white{% else %}black{% endif %}';">
                {{ ind | title }}
            </a>
        {% endfor %}
    </div>
</div>

<p>Visualizing: <strong>{{ title }}</strong></p>

<div style="height: 600px; border: 1px solid #ccc; border-radius: 8px; overflow: hidden;">
    {{ map | safe }}
</div>

<div style="margin-top: 20px; background: #f5f5f5; padding: 15px; border-radius: 8px;">
    <h4>About This Map</h4>
    <p>This choropleth map shows {{ title | lower }} across Malawi's districts. 
    Darker colors represent higher values.</p>
</div>
{% endblock %}
```

**End of Day 13:**
- [ ] Commit to GitHub: "Add dynamic indicator switching for choropleth"
- [ ] Test: click between population, literacy, healthcare
- [ ] Map updates correctly with different color scales

---

### Day 14: Heatmaps & Cluster Maps

**Morning (2–3 hrs):**
- [ ] Learn about heatmaps (point density visualization)
- [ ] Learn about marker clusters (group nearby points)
- [ ] Create sample point data (hospitals, schools, water points)

**Code (`data/sample_points.py` - generate sample data):**
```python
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import random

# Generate sample point data for Malawi
random.seed(42)

points_data = {
    'name': [],
    'type': [],
    'latitude': [],
    'longitude': [],
    'visit_count': []
}

# Define regions with approximate bounds
regions = {
    'North': {'lat': (-11.0, -10.5), 'lon': (33.5, 34.5)},
    'Central': {'lat': (-14.0, -13.0), 'lon': (33.5, 35.5)},
    'South': {'lat': (-17.0, -15.5), 'lon': (34.5, 35.5)}
}

facility_types = ['Hospital', 'Health Center', 'School', 'Water Point', 'Market']

for region, bounds in regions.items():
    for i in range(20):  # 20 points per region
        lat = random.uniform(bounds['lat'][0], bounds['lat'][1])
        lon = random.uniform(bounds['lon'][0], bounds['lon'][1])
        facility = random.choice(facility_types)
        
        points_data['name'].append(f"{facility} {region} {i}")
        points_data['type'].append(facility)
        points_data['latitude'].append(lat)
        points_data['longitude'].append(lon)
        points_data['visit_count'].append(random.randint(1, 100))

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(
    pd.DataFrame(points_data),
    geometry=[Point(lon, lat) for lat, lon in zip(
        points_data['latitude'],
        points_data['longitude']
    )],
    crs='EPSG:4326'
)

# Save to GeoJSON
gdf.to_file('data/sample_facilities.geojson', driver='GeoJSON')
print(f"Created {len(gdf)} sample facilities")
print(gdf.head())
```

**Run:**
```bash
python data/sample_points.py
```

**Afternoon (2–3 hrs):**
- [ ] Create heatmap route
- [ ] Create cluster map route
- [ ] Test both visualizations

**Code (`app.py` - add new routes):**
```python
@app.route('/heatmap')
def heatmap_view():
    """Display heatmap of point density"""
    
    # Load points
    points = gpd.read_file('data/sample_facilities.geojson')
    
    # Create map
    m = folium.Map(
        location=[-13.3, 34.3],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Convert to list of [lat, lon] for heatmap
    heat_data = [[row['latitude'], row['longitude']] for idx, row in points.iterrows()]
    
    # Add heatmap layer
    folium.plugins.HeatMap(
        heat_data,
        radius=25,
        blur=15,
        max_zoom=1,
        name='Facility Density'
    ).add_to(m)
    
    folium.LayerControl().add_to(m)
    map_html = m._repr_html_()
    
    return render_template('heatmap.html', map=map_html)

@app.route('/clusters')
def cluster_map():
    """Display marker cluster map"""
    
    # Load points
    points = gpd.read_file('data/sample_facilities.geojson')
    
    # Create map
    m = folium.Map(
        location=[-13.3, 34.3],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Add marker cluster
    marker_cluster = folium.plugins.MarkerCluster(name='Clustered Facilities').add_to(m)
    
    # Add each facility as marker
    facility_colors = {
        'Hospital': 'red',
        'Health Center': 'orange',
        'School': 'blue',
        'Water Point': 'lightblue',
        'Market': 'green'
    }
    
    for idx, row in points.iterrows():
        color = facility_colors.get(row['type'], 'gray')
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['name']}<br>Type: {row['type']}",
            tooltip=row['name'],
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(marker_cluster)
    
    folium.LayerControl().add_to(m)
    map_html = m._repr_html_()
    
    return render_template('cluster.html', map=map_html)
```

**Note:** Add imports at top of `app.py`:
```python
import folium.plugins
```

**Templates:**

`templates/heatmap.html`:
```html
{% extends "base.html" %}

{% block content %}
<h1>Facility Density Heatmap</h1>
<p>This heatmap shows the concentration of health facilities, schools, and other services across Malawi.</p>
<div style="height: 600px; border: 1px solid #ccc; border-radius: 8px; overflow: hidden;">
    {{ map | safe }}
</div>
{% endblock %}
```

`templates/cluster.html`:
```html
{% extends "base.html" %}

{% block content %}
<h1>Clustered Facilities Map</h1>
<p>This map groups nearby facilities for easier navigation. Click clusters to zoom in.</p>
<div style="height: 600px; border: 1px solid #ccc; border-radius: 8px; overflow: hidden;">
    {{ map | safe }}
</div>
{% endblock %}
```

**End of Day 14:**
- [ ] Commit to GitHub: "Add heatmap and cluster map visualizations"
- [ ] Test both new routes
- [ ] Verify sample_facilities.geojson created correctly

---

### Day 15: Integration & Testing

**Morning (2–3 hrs):**
- [ ] Add navigation menu linking to all map types
- [ ] Update homepage with overview of visualizations
- [ ] Test all routes work correctly

**Code (`templates/index.html` - updated):**
```html
{% extends "base.html" %}

{% block content %}
<h1>Welcome to Geospatial Web Mapping</h1>

<p>Interactive mapping tools for spatial data exploration and analysis.</p>

<h2>Available Visualizations</h2>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0;">
    
    <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <h3>📍 District Map</h3>
        <p>View and filter Malawi districts by region with statistics.</p>
        <a href="/map" style="color: #667eea; text-decoration: none; font-weight: bold;">View →</a>
    </div>
    
    <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <h3>🎨 Choropleth Map</h3>
        <p>Visualize population and statistics by district with color coding.</p>
        <a href="/choropleth" style="color: #667eea; text-decoration: none; font-weight: bold;">View →</a>
    </div>
    
    <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <h3>🔥 Heatmap</h3>
        <p>Density map showing facility concentration across regions.</p>
        <a href="/heatmap" style="color: #667eea; text-decoration: none; font-weight: bold;">View →</a>
    </div>
    
    <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <h3>📌 Cluster Map</h3>
        <p>Grouped markers for facility locations with zoom capability.</p>
        <a href="/clusters" style="color: #667eea; text-decoration: none; font-weight: bold;">View →</a>
    </div>
</div>

<h2>Technologies Used</h2>
<ul>
    <li><strong>Flask</strong> - Python web framework</li>
    <li><strong>Folium</strong> - Interactive maps</li>
    <li><strong>GeoPandas</strong> - Spatial data analysis</li>
    <li><strong>Leaflet.js</strong> - Underlying mapping library</li>
</ul>

{% endblock %}
```

**Afternoon (2–3 hrs):**
- [ ] Test all routes: `/`, `/map`, `/choropleth`, `/heatmap`, `/clusters`
- [ ] Test navigation works smoothly
- [ ] Verify all maps render without errors
- [ ] Check responsive design on mobile

**Test checklist:**
```bash
# Start server
python app.py

# Test each route in browser:
# http://localhost:5000/              → Home page
# http://localhost:5000/map           → Districts
# http://localhost:5000/map?region=North   → Filtered
# http://localhost:5000/choropleth    → Choropleth
# http://localhost:5000/choropleth?indicator=literacy  → Different indicator
# http://localhost:5000/heatmap       → Heatmap
# http://localhost:5000/clusters      → Clusters
```

**End of Day 15:**
- [ ] Commit to GitHub: "Integrate all visualizations, update homepage"
- [ ] All routes tested and working
- [ ] Homepage displays cards linking to visualizations

---

## Week 3 Checklist

- [ ] Spatial operations module created (buffer, intersect, dissolve, etc.)
- [ ] Spatial operations tested with sample data
- [ ] Choropleth map implemented (single indicator)
- [ ] Multiple indicators for choropleth switching
- [ ] Heatmap visualization created
- [ ] Cluster map visualization created
- [ ] Sample point data generated
- [ ] All routes tested and working
- [ ] Homepage redesigned with visualization cards
- [ ] Navigation menu updated
- [ ] Responsive design verified
- [ ] All code committed to GitHub

---

## Week 3 Summary

**Skills Gained:**
- GeoPandas spatial operations (buffer, intersect, dissolve)
- Choropleth map creation in Folium
- Dynamic indicator switching
- Heatmaps and marker clustering
- Multiple visualization types

**Code Created:**
- `geo_utils/spatial_ops.py` (utility functions)
- Choropleth route with multi-indicator support
- Heatmap route
- Cluster map route
- Sample data generator
- Updated homepage with visualization cards

**Deliverables:**
- 4 different geospatial visualizations
- Dynamic data switching (indicators)
- Interactive maps with popups and clustering

**GitHub Commits:**
- "Add spatial operations utility module"
- "Add choropleth map route and template"
- "Add dynamic indicator switching for choropleth"
- "Add heatmap and cluster map visualizations"
- "Integrate all visualizations, update homepage"

**Time Spent:** _____ hours

**Blockers Encountered:**
_________________________________________________________________

**Lessons Learned:**
_________________________________________________________________

**Next Week Preview:**
Week 4 will focus on PostGIS integration, database queries, and scalable data handling for larger datasets.

---

## Resources Used This Week

- GeoPandas Spatial Operations: https://geopandas.org/docs/user_guide/geometric_operations.html
- Folium Choropleth: https://python-visualization.github.io/folium/latest/user_guide/GeoData.html
- Folium Heatmap Plugin: https://python-visualization.github.io/folium/plugins.html#folium.plugins.HeatMap
- Folium MarkerCluster: https://python-visualization.github.io/folium/plugins.html#folium.plugins.MarkerCluster
- Shapely Geometry: https://shapely.readthedocs.io/

**Questions to explore next week:**
- How do I load large shapefiles efficiently?
- How do I connect to PostGIS?
- How do I cache map tiles for faster loading?
- How do I implement real-time data updates?
